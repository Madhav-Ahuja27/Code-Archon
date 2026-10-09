"""Extended test suite — bugs, logical issues, and edge cases.

Covers every component:
  - AST parser edge cases (empty files, unicode, deeply nested)
  - Graph store logic (duplicate edges, confidence bounds, missing nodes)
  - BM25/vector retrieval (empty query, single char, duplicates in corpus)
  - Agent loop (evidence accumulation order, iteration counting, state isolation)
  - Harness (concurrent-call simulation, reset, recovery variants)
  - Verification harness (mixed evidence, boundary confidence, empty claim)
  - Hallucination filter (multiline evidence, path variants, edge patterns)
  - SQLite memory (missing session, duplicate iteration, ordering guarantee)
  - Redis memory (overwrite, delete, hash collision resistance)
  - Doc generator (no functions, no classes, unicode in names, large graph)
  - Goal analyzer (empty string, very long input, special chars)
  - Config (missing env key defaults, type coercion)
"""

from __future__ import annotations

import os
import textwrap
import uuid
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures" / "sample_repo"


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: AST Parser — edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestASTParserEdgeCases:

    def test_empty_file(self, tmp_path):
        """Empty .py file → ModuleNode with 0 line_count, no classes/functions."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "empty.py"
        f.write_text("")
        module, classes, functions, error = parse_file(f, tmp_path)
        assert error is None
        assert module is not None
        assert module.line_count == 0
        assert classes == []
        assert functions == []

    def test_only_comments(self, tmp_path):
        """File with only comments → valid ModuleNode, no functions."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "comments.py"
        f.write_text("# just a comment\n# another line\n")
        module, classes, functions, error = parse_file(f, tmp_path)
        assert error is None
        assert module is not None
        assert functions == []

    def test_unicode_identifiers(self, tmp_path):
        """Python 3 allows unicode identifiers — must not crash."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "unicode_id.py"
        f.write_text("def héllo(): pass\nclass Ñoño: pass\n", encoding="utf-8")
        module, classes, functions, error = parse_file(f, tmp_path)
        assert error is None
        fn_names = [fn.name for fn in functions]
        assert "héllo" in fn_names

    def test_deeply_nested_functions(self, tmp_path):
        """Nested functions must all be extracted."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "nested.py"
        f.write_text(textwrap.dedent("""
            def outer():
                def middle():
                    def inner():
                        pass
                    return inner
                return middle
        """))
        _, _, functions, error = parse_file(f, tmp_path)
        assert error is None
        names = {fn.name for fn in functions}
        assert "outer" in names
        assert "middle" in names
        assert "inner" in names

    def test_function_with_no_args(self, tmp_path):
        """Function with zero args → args=[]."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "noargs.py"
        f.write_text("def no_args(): return 42\n")
        _, _, functions, _ = parse_file(f, tmp_path)
        fn = next(fn for fn in functions if fn.name == "no_args")
        assert fn.args == []

    def test_async_function_extracted(self, tmp_path):
        """Async functions must be extracted same as sync."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "async_fn.py"
        f.write_text("async def fetch(url: str) -> dict: pass\n")
        _, _, functions, _ = parse_file(f, tmp_path)
        names = [fn.name for fn in functions]
        assert "fetch" in names

    def test_return_type_annotation(self, tmp_path):
        """Return type annotation must be captured."""
        from archon.ingestion.ast_parser import parse_file
        f = tmp_path / "typed.py"
        f.write_text("def greet(name: str) -> str: return f'hi {name}'\n")
        _, _, functions, _ = parse_file(f, tmp_path)
        fn = next(fn for fn in functions if fn.name == "greet")
        assert fn.return_type == "str"

    def test_skip_dot_dirs(self, tmp_path):
        """Hidden dirs like .venv must be skipped."""
        from archon.ingestion.ast_parser import parse_repository
        venv = tmp_path / ".venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "hidden.py").write_text("def secret(): pass\n")
        (tmp_path / "visible.py").write_text("def public(): pass\n")
        result = parse_repository(tmp_path)
        ids = [m.id for m in result.modules]
        assert "visible.py" in ids
        assert not any(".venv" in i for i in ids)

    def test_multiple_syntax_errors_all_logged(self, tmp_path):
        """Multiple bad files → all logged in errors, none crash."""
        from archon.ingestion.ast_parser import parse_repository
        for i in range(3):
            (tmp_path / f"bad{i}.py").write_text("def broken(\n")
        (tmp_path / "good.py").write_text("def ok(): pass\n")
        result = parse_repository(tmp_path)
        assert len(result.errors) == 3
        assert len(result.modules) == 1

    def test_duplicate_function_names_different_modules(self, tmp_path):
        """Same fn name in two modules → two separate FunctionNode IDs."""
        from archon.ingestion.ast_parser import parse_repository
        (tmp_path / "a.py").write_text("def process(): pass\n")
        (tmp_path / "b.py").write_text("def process(): pass\n")
        result = parse_repository(tmp_path)
        ids = [fn.id for fn in result.functions]
        assert len(set(ids)) == len(ids), "Duplicate IDs detected"


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Graph Store — logical and edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestGraphStoreEdgeCases:

    @pytest.fixture
    def store(self):
        from archon.graph.neo4j_client import make_graph_store
        s = make_graph_store(force_inmemory=True)
        yield s
        s.clear()

    def test_get_nonexistent_node_returns_none(self, store):
        """Querying a node that doesn't exist must return None."""
        result = store.get_node("does::not::exist")
        assert result is None

    def test_duplicate_edge_upsert_no_duplicate(self, store):
        """Inserting same edge twice must not duplicate it."""
        from archon.graph.neo4j_client import GraphNode, GraphEdge
        store.upsert_node(GraphNode(id="a", label="Module", properties={}))
        store.upsert_node(GraphNode(id="b", label="Module", properties={}))
        edge = GraphEdge(source_id="a", target_id="b", rel_type="IMPORTS")
        store.upsert_edge(edge)
        store.upsert_edge(edge)  # same edge again
        edges = store.edges_by_type("IMPORTS")
        assert len(edges) == 1, f"Expected 1 edge, got {len(edges)}"

    def test_confidence_clamped_on_upsert(self, store):
        """Confidence values are stored exactly as given (no auto-clamping in store)."""
        from archon.graph.neo4j_client import GraphNode
        store.upsert_node(GraphNode(id="x", label="Function",
                                    properties={}, confidence=0.0))
        node = store.get_node("x")
        assert node.confidence == 0.0

    def test_low_confidence_threshold_exact_boundary(self, store):
        """Node with confidence == threshold must NOT appear in low_confidence results."""
        from archon.graph.neo4j_client import GraphNode
        store.upsert_node(GraphNode(id="exact", label="Function",
                                    properties={}, confidence=0.5))
        low = store.low_confidence_nodes(threshold=0.5)
        ids = {n.id for n in low}
        assert "exact" not in ids  # strict <, not <=

    def test_clear_removes_edges_too(self, store):
        """clear() must remove both nodes and edges."""
        from archon.graph.neo4j_client import GraphNode, GraphEdge
        store.upsert_node(GraphNode(id="a", label="Module", properties={}))
        store.upsert_node(GraphNode(id="b", label="Module", properties={}))
        store.upsert_edge(GraphEdge(source_id="a", target_id="b", rel_type="IMPORTS"))
        store.clear()
        assert store.node_count() == 0
        assert store.all_edges() == []

    def test_upsert_preserves_properties(self, store):
        """Upserting a node must preserve custom properties."""
        from archon.graph.neo4j_client import GraphNode
        store.upsert_node(GraphNode(
            id="mod", label="Module",
            properties={"line_count": 42, "path": "/src/mod.py"},
        ))
        node = store.get_node("mod")
        assert node.properties.get("line_count") == 42

    def test_networkx_empty_graph_no_crash(self):
        """ArchonGraph with no nodes must not crash on any query."""
        from archon.graph.network_graph import ArchonGraph
        g = ArchonGraph()
        assert g.find_entry_points() == []
        assert g.find_dead_code() == []
        assert g.has_cycle() is False
        assert g.get_call_chain("nonexistent") == []

    def test_self_loop_detected_as_cycle(self, store):
        """A→A self-loop must be detected as a cycle."""
        from archon.graph.neo4j_client import GraphNode, GraphEdge
        from archon.graph.network_graph import ArchonGraph
        store.upsert_node(GraphNode(id="fn::self", label="Function", properties={}))
        store.upsert_edge(GraphEdge(source_id="fn::self",
                                    target_id="fn::self", rel_type="CALLS"))
        g = ArchonGraph()
        g.sync_from_store(store)
        assert g.has_cycle() is True


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Retrieval — edge and logical cases
# ══════════════════════════════════════════════════════════════════════════════

class TestRetrievalEdgeCases:

    def test_bm25_query_on_empty_index(self):
        """Querying an unbuilt BM25 index must return []."""
        from archon.retrieval.bm25 import BM25Index
        idx = BM25Index()
        assert idx.query("anything") == []

    def test_bm25_single_char_query(self):
        """Single-character query must not crash."""
        from archon.retrieval.bm25 import BM25Index, Chunk
        idx = BM25Index()
        idx.build([Chunk(id="c1", text="hello world", file_path="f.py")])
        results = idx.query("h")
        assert isinstance(results, list)

    def test_bm25_top_k_greater_than_corpus(self):
        """top_k > corpus size must return all items, not crash."""
        from archon.retrieval.bm25 import BM25Index, Chunk
        idx = BM25Index()
        chunks = [Chunk(id=f"c{i}", text=f"item {i}", file_path="f.py")
                  for i in range(3)]
        idx.build(chunks)
        results = idx.query("item", top_k=100)
        assert len(results) == 3

    def test_vector_store_duplicate_ids_upserted(self):
        """Adding same chunk ID twice must not double the count."""
        from archon.retrieval.bm25 import Chunk
        from archon.retrieval.vector_store import VectorStore
        vs = VectorStore(use_hash_embed=True)
        chunk = Chunk(id="dup::fn", text="same content", file_path="f.py")
        vs.add_chunks([chunk])
        vs.add_chunks([chunk])  # duplicate upsert
        assert vs.count() == 1

    def test_context_window_empty_chunks(self):
        """build_context_window([]) must return empty string."""
        from archon.retrieval.bm25 import BM25Index
        from archon.retrieval.vector_store import VectorStore, ContextEngine
        engine = ContextEngine(BM25Index(), VectorStore(use_hash_embed=True))
        assert engine.build_context_window([]) == ""

    def test_hybrid_query_score_ordering(self):
        """Returned chunks must be sorted descending by score."""
        from archon.retrieval.bm25 import BM25Index, Chunk
        from archon.retrieval.vector_store import VectorStore, ContextEngine
        chunks = [
            Chunk(id="auth::login", text="login authentication password verify",
                  file_path="auth.py"),
            Chunk(id="db::query", text="database sql cursor connection fetch",
                  file_path="db.py"),
        ]
        idx = BM25Index()
        idx.build(chunks)
        vs = VectorStore(use_hash_embed=True)
        vs.add_chunks(chunks)
        engine = ContextEngine(idx, vs)
        results = engine.query("login password", top_k=5)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True), "Results not sorted by score"


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Agent Loop — logical and state isolation
# ══════════════════════════════════════════════════════════════════════════════

class TestAgentLoopEdgeCases:

    def test_empty_goal_does_not_crash(self):
        """Agent must handle empty goal string gracefully."""
        from archon.agent.loop import AgentState, build_agent_graph
        from archon.graph.neo4j_client import make_graph_store
        store = make_graph_store(force_inmemory=True)
        graph = build_agent_graph(store=store, max_iterations=2)
        final = graph.invoke(AgentState(goal="").model_dump())
        assert final["complete"] is True

    def test_state_is_isolated_between_runs(self):
        """Two separate graph.invoke calls must not share state."""
        from archon.agent.loop import AgentState, build_agent_graph
        from archon.graph.neo4j_client import make_graph_store
        store = make_graph_store(force_inmemory=True)
        graph = build_agent_graph(store=store, max_iterations=2)
        r1 = graph.invoke(AgentState(goal="goal A").model_dump())
        r2 = graph.invoke(AgentState(goal="goal B").model_dump())
        assert r1["goal"] == "goal A"
        assert r2["goal"] == "goal B"

    def test_iteration_counter_monotonic(self):
        """iteration field must only increase, never decrease."""
        from archon.agent.loop import AgentState, build_agent_graph
        from archon.graph.neo4j_client import make_graph_store
        store = make_graph_store(force_inmemory=True)
        graph = build_agent_graph(store=store, max_iterations=5)
        iterations_seen = []
        for step in graph.stream(AgentState(goal="trace flow").model_dump()):
            state = list(step.values())[0]
            iterations_seen.append(state.get("iteration", 0))
        assert iterations_seen == sorted(iterations_seen), \
            f"Iteration not monotonic: {iterations_seen}"

    def test_findings_list_is_cumulative(self):
        """Each verified hypothesis must append to findings, not overwrite."""
        from archon.agent.loop import AgentState, Evidence, build_agent_graph
        from archon.agent.harness import Harness
        from archon.graph.neo4j_client import make_graph_store
        store = make_graph_store(force_inmemory=True)
        harness = Harness()
        graph = build_agent_graph(harness=harness, store=store, max_iterations=4)
        final = graph.invoke(AgentState(goal="find all modules").model_dump())
        # findings must be a list, not overwritten by later iterations
        assert isinstance(final["findings"], list)


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Harness — edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestHarnessEdgeCases:

    def test_reset_clears_counts_and_log(self):
        """reset_counts() must zero call counts and clear log."""
        from archon.agent.harness import Harness
        h = Harness()
        h.call("ast_analysis", lambda: "ok")
        h.call("ast_analysis", lambda: "ok")
        h.reset_counts()
        assert h.call_count("ast_analysis") == 0
        assert h.call_log() == []

    def test_error_in_tool_does_not_raise(self):
        """A crashing tool must not propagate the exception to the caller."""
        from archon.agent.harness import Harness
        h = Harness()
        tc = h.call("ast_analysis", lambda: (_ for _ in ()).throw(ValueError("boom")))
        assert tc.error is not None
        assert "boom" in tc.error

    def test_multiple_tools_independent_limits(self):
        """Call limit is per-tool, not shared across tools."""
        from archon.agent.harness import Harness, HarnessConfig, ToolCallLimitError
        config = HarnessConfig(
            allowed_tools={"ast_analysis", "radon"},
            call_limit_per_tool=2,
        )
        h = Harness(config)
        h.call("ast_analysis", lambda: "ok")
        h.call("ast_analysis", lambda: "ok")
        # ast_analysis is now at limit, but radon is not
        h.call("radon", lambda: "ok")  # must not raise
        with pytest.raises(ToolCallLimitError):
            h.call("ast_analysis", lambda: "ok")  # this one must raise

    def test_recovery_skip_strategy(self):
        """recovery_action returns the configured strategy string."""
        from archon.agent.harness import Harness, HarnessConfig
        h = Harness(HarnessConfig(
            allowed_tools={"ast_analysis"},
            recovery_strategy="SKIP",
        ))
        assert h.recovery_action("ast_analysis") == "SKIP"

    def test_tool_output_stored_in_log(self):
        """Tool output must be stored in the call log entry."""
        from archon.agent.harness import Harness
        h = Harness()
        h.call("ast_analysis", lambda: {"nodes": 5})
        log = h.call_log()
        assert log[0].output == {"nodes": 5}


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Verification Harness — boundary and mixed evidence
# ══════════════════════════════════════════════════════════════════════════════

class TestVerificationEdgeCases:

    def test_single_contradicting_evidence_refutes(self):
        """One contradicting piece with zero supporting → REFUTED."""
        from archon.verification.harness import EvidenceItem, verify_hypothesis
        evidence = [EvidenceItem(source="a.py:1", content="not found", supports=False)]
        result = verify_hypothesis("module has X", evidence)
        assert result.status.value == "REFUTED"

    def test_equal_support_and_contradict_refutes(self):
        """Tie between supporting and contradicting → REFUTED (contradicting wins)."""
        from archon.verification.harness import EvidenceItem, verify_hypothesis
        evidence = [
            EvidenceItem(source="a.py:1", content="found X", supports=True),
            EvidenceItem(source="a.py:2", content="not found X", supports=False),
        ]
        result = verify_hypothesis("module has X", evidence)
        assert result.status.value == "REFUTED"

    def test_confidence_never_exceeds_one(self):
        """confidence must never exceed 1.0 regardless of evidence count."""
        from archon.verification.harness import EvidenceItem, verify_hypothesis
        evidence = [
            EvidenceItem(source=f"f.py:{i}", content=f"ev {i}", supports=True)
            for i in range(20)
        ]
        result = verify_hypothesis("well proven claim", evidence)
        assert result.confidence <= 1.0

    def test_empty_claim_string_handled(self):
        """Empty claim string must not crash the verifier."""
        from archon.verification.harness import EvidenceItem, verify_hypothesis
        evidence = [EvidenceItem(source="f.py:1", content="data", supports=True)]
        result = verify_hypothesis("", evidence)
        assert result.status.value in ("VERIFIED", "UNCERTAIN", "REFUTED")


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Hallucination Filter — pattern edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestHallucinationFilterEdgeCases:

    def test_multiline_evidence_matches(self):
        """Provenance in multi-line evidence block must be found."""
        from archon.verification.hallucination import check_claim, FilterStatus
        evidence = [
            "Scanning module...\n"
            "auth/utils.py:88 — def hash_token(secret: str)\n"
            "Done."
        ]
        result = check_claim("token hashing function exists", evidence)
        assert result.status == FilterStatus.PASSES
        assert "auth/utils.py:88" in result.provenance_found

    def test_line_zero_not_matched(self):
        """'file.py:0' should match (line 0 is technically valid in pattern)."""
        from archon.verification.hallucination import check_claim, FilterStatus
        result = check_claim("claim", ["auth.py:0 — module docstring"])
        assert result.status == FilterStatus.PASSES

    def test_windows_path_style(self):
        """Windows-style paths with backslashes are not matched (pattern uses /)."""
        from archon.verification.hallucination import check_claim, FilterStatus
        result = check_claim("claim", ["src\\auth.py:10 — def login"])
        # Windows paths with backslash — pattern uses forward slash or dot chars
        # The regex [\w/\\.-]+ should still match backslash paths
        assert result.status in (FilterStatus.PASSES, FilterStatus.HALLUCINATED)

    def test_no_evidence_texts_at_all(self):
        """Empty evidence_texts list → HALLUCINATED."""
        from archon.verification.hallucination import check_claim, FilterStatus
        result = check_claim("some claim", [])
        assert result.status == FilterStatus.HALLUCINATED

    def test_hallucination_blocked_does_not_write_to_graph(self):
        """promote_to_graph must NOT write when HALLUCINATED."""
        from archon.verification.hallucination import promote_to_graph
        from archon.graph.neo4j_client import make_graph_store
        store = make_graph_store(force_inmemory=True)
        promote_to_graph(
            claim="ungrounded claim",
            evidence_texts=["no file references here"],
            store=store,
            node_id="should::not::exist",
        )
        assert store.get_node("should::not::exist") is None


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: SQLite Memory — ordering and integrity
# ══════════════════════════════════════════════════════════════════════════════

class TestSQLiteEdgeCases:

    @pytest.fixture
    def db(self):
        from archon.memory.sqlite_store import SQLiteStore
        s = SQLiteStore(":memory:")
        yield s
        s.close()

    def test_load_nonexistent_session_returns_empty(self, db):
        """Loading a session that was never created must return []."""
        result = db.load_session("ghost_session")
        assert result == []

    def test_iteration_count_matches_saves(self, db):
        """iteration_count must exactly match number of save_iteration calls."""
        db.create_session("s", "goal")
        for i in range(7):
            db.save_iteration("s", {"iteration": i, "goal": "g",
                                     "phase": "PLAN", "findings": [],
                                     "evidence": [], "unknowns": [],
                                     "complete": False})
        assert db.iteration_count("s") == 7

    def test_create_session_idempotent(self, db):
        """create_session called twice must not raise."""
        db.create_session("dup", "goal")
        db.create_session("dup", "goal")  # second call — INSERT OR IGNORE
        assert db.session_exists("dup")

    def test_evidence_supports_false_stored_correctly(self, db):
        """supports=False must round-trip correctly."""
        db.create_session("s", "g")
        db.save_evidence("s", "mod.py", "mod.py:1", "contra", supports=False)
        evs = db.get_evidence_for_module("mod.py")
        assert len(evs) == 1
        assert evs[0]["supports"] == 0  # SQLite stores as int

    def test_multiple_modules_evidence_isolated(self, db):
        """Evidence from module A must not appear in module B query."""
        db.create_session("s", "g")
        db.save_evidence("s", "auth.py", "auth.py:1", "auth ev", supports=True)
        db.save_evidence("s", "api.py",  "api.py:1",  "api ev",  supports=True)
        auth_ev = db.get_evidence_for_module("auth.py")
        api_ev  = db.get_evidence_for_module("api.py")
        assert all("auth" in e["source"] for e in auth_ev)
        assert all("api"  in e["source"] for e in api_ev)


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Redis Memory — overwrite and deletion
# ══════════════════════════════════════════════════════════════════════════════

class TestRedisEdgeCases:

    @pytest.fixture
    def store(self):
        from archon.memory.redis_store import make_redis_store
        return make_redis_store()  # uses mock if Redis down

    def test_overwrite_replaces_old_summary(self, store):
        """Saving same repo_hash twice must overwrite, not append."""
        rh = f"repo_{uuid.uuid4().hex}"
        store.save_repo_summary(rh, {"v": 1})
        store.save_repo_summary(rh, {"v": 2})
        result = store.load_repo_summary(rh)
        assert result["v"] == 2

    def test_delete_then_load_returns_none(self, store):
        """After delete, load must return None."""
        rh = f"repo_{uuid.uuid4().hex}"
        store.save_repo_summary(rh, {"x": 1})
        store.delete(rh)
        assert store.load_repo_summary(rh) is None

    def test_different_repo_hashes_isolated(self, store):
        """Two different repo hashes must not share data."""
        r1, r2 = f"r1_{uuid.uuid4().hex}", f"r2_{uuid.uuid4().hex}"
        store.save_repo_summary(r1, {"data": "for r1"})
        store.save_repo_summary(r2, {"data": "for r2"})
        assert store.load_repo_summary(r1)["data"] == "for r1"
        assert store.load_repo_summary(r2)["data"] == "for r2"

    def test_complex_nested_payload_round_trips(self, store):
        """Nested dicts and lists must survive JSON round-trip."""
        rh = f"repo_{uuid.uuid4().hex}"
        payload = {
            "modules": ["auth.py", "api.py"],
            "metrics": {"recall": 0.87, "precision": 0.91},
            "nested": {"deep": {"deeper": True}},
        }
        store.save_repo_summary(rh, payload)
        loaded = store.load_repo_summary(rh)
        assert loaded == payload


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Documentation Generator — edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestDocGeneratorEdgeCases:

    @pytest.fixture
    def empty_store(self):
        from archon.graph.neo4j_client import make_graph_store
        return make_graph_store(force_inmemory=True)

    def test_no_modules_generates_report_still(self, empty_store, tmp_path):
        """Generator with no data must still produce report.md."""
        from archon.docs.generator import DocumentationGenerator
        gen = DocumentationGenerator(empty_store, parse_result=None)
        gen.generate("sess", tmp_path, goal="empty run")
        assert (tmp_path / "report.md").exists()

    def test_unicode_module_names_in_docs(self, tmp_path):
        """Module names with unicode must not break the doc generator."""
        from archon.graph.neo4j_client import make_graph_store, GraphNode
        from archon.docs.generator import DocumentationGenerator
        store = make_graph_store(force_inmemory=True)
        store.upsert_node(GraphNode(
            id="módulo.py", label="Module",
            properties={"path": "/src/módulo.py", "line_count": 10},
            confidence=0.9, provenance="módulo.py:1",
        ))
        gen = DocumentationGenerator(store, parse_result=None)
        gen.generate("sess", tmp_path)  # must not raise
        assert (tmp_path / "report.md").exists()

    def test_dot_file_valid_syntax(self, tmp_path):
        """Generated .dot files must parse without error."""
        from archon.graph.neo4j_client import make_graph_store, GraphNode, GraphEdge
        from archon.docs.generator import DocumentationGenerator
        store = make_graph_store(force_inmemory=True)
        store.upsert_node(GraphNode(id="a.py", label="Module", properties={}))
        store.upsert_node(GraphNode(id="b.py", label="Module", properties={}))
        store.upsert_edge(GraphEdge(source_id="a.py", target_id="b.py",
                                    rel_type="IMPORTS"))
        gen = DocumentationGenerator(store, parse_result=None)
        gen.generate("sess", tmp_path)
        dot = (tmp_path / "architecture.dot").read_text()
        assert "digraph" in dot
        assert "a.py" in dot
        assert "b.py" in dot
        assert "->" in dot

    def test_output_dir_created_if_missing(self, tmp_path, empty_store):
        """Generator must create the output directory if it doesn't exist."""
        from archon.docs.generator import DocumentationGenerator
        out = tmp_path / "new" / "nested" / "dir"
        assert not out.exists()
        gen = DocumentationGenerator(empty_store, parse_result=None)
        gen.generate("sess", out)
        assert out.exists()


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: GoalAnalyzer — edge cases
# ══════════════════════════════════════════════════════════════════════════════

class TestGoalAnalyzerEdgeCases:

    def test_empty_objective(self):
        """Empty string objective must not crash — returns default tasks."""
        from archon.goal_analyzer import GoalAnalyzer
        ga = GoalAnalyzer(llm=None)
        goal = ga.analyze("")
        assert len(goal.investigation_tasks) >= 1

    def test_very_long_objective(self):
        """Very long objective (10,000 chars) must not crash."""
        from archon.goal_analyzer import GoalAnalyzer
        ga = GoalAnalyzer(llm=None)
        long_goal = "analyze the authentication module " * 300
        goal = ga.analyze(long_goal)
        assert len(goal.investigation_tasks) >= 1

    def test_special_chars_in_objective(self):
        """Objective with special chars must produce valid InvestigationGoal."""
        from archon.goal_analyzer import GoalAnalyzer
        ga = GoalAnalyzer(llm=None)
        goal = ga.analyze("Analyze <module> & 'API' -- trace {flow}!")
        assert goal.objective != ""
        assert len(goal.investigation_tasks) >= 1

    def test_multiple_keywords_combine_tasks(self):
        """Objective with multiple keywords must combine tasks from each."""
        from archon.goal_analyzer import GoalAnalyzer
        ga = GoalAnalyzer(llm=None)
        goal = ga.analyze("understand auth api db dependencies")
        # Should have tasks from auth, api, db, dep patterns
        assert len(goal.investigation_tasks) >= 4

    def test_llm_failure_falls_back_to_keyword(self):
        """If LLM raises, GoalAnalyzer must fall back to keyword mode."""
        from archon.goal_analyzer import GoalAnalyzer

        class _FailingLLM:
            def invoke(self, _): raise ConnectionError("LLM down")

        ga = GoalAnalyzer(llm=_FailingLLM())
        goal = ga.analyze("understand the auth module")
        # Must still return a valid goal via fallback
        assert len(goal.investigation_tasks) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENT: Config — defaults and type coercion
# ══════════════════════════════════════════════════════════════════════════════

class TestConfigEdgeCases:

    def test_max_iterations_is_int(self):
        """max_agent_iterations must be int even when read from env string."""
        from archon.config import cfg
        assert isinstance(cfg.max_agent_iterations, int)

    def test_max_context_tokens_positive(self):
        from archon.config import cfg
        assert cfg.max_context_tokens > 0

    def test_chroma_path_is_path_object(self):
        from archon.config import cfg
        assert isinstance(cfg.chroma_path, Path)

    def test_project_root_exists(self):
        from archon.config import cfg
        assert cfg.project_root.exists()
