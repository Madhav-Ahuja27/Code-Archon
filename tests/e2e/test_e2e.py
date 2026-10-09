"""Phase 9 — End-to-End Integration tests.

test_full_pipeline_fixture  — runs the complete pipeline on the sample_repo
                              fixture using a mock LLM (works offline/sandbox).
test_groq_goal_analyzer     — calls real Groq API (skipped if unreachable).
test_groq_verify            — calls real Groq to verify a hypothesis (skipped if unreachable).

Gate: pipeline test passes + eval metrics met.
"""

from __future__ import annotations

import socket
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"
OUTPUT = Path(__file__).parent.parent.parent / "output" / "e2e_test"


# ── Mock LLM ─────────────────────────────────────────────────────────────────

class _MockLLM:
    """Deterministic mock — no network required."""

    def invoke(self, messages):
        import re
        system = str(messages[0].content) if messages else ""
        human = str(messages[-1].content) if messages else ""
        if "code archaeologist" in system:       # cite a real source from the evidence
            m = re.search(r"\[([\w/.\\-]+\.py:\d+)\]", human)
            return _Resp(f"Authentication logic lives in {m.group(1)}." if m else "INSUFFICIENT")
        if "ONLY one word" in system:
            return _Resp("VERIFIED")
        return _Resp(
            '{"objective": "understand codebase", '
            '"focus_modules": ["auth.py", "api.py"], '
            '"investigation_tasks": ["map module structure", "trace auth flow", '
            '"identify entry points"], '
            '"success_criteria": ["All modules documented", "Call chain traced"]}'
        )

class _Resp:
    def __init__(self, content): self.content = content


def _groq_reachable() -> bool:
    """Check if Groq API is actually callable (not just TCP-reachable)."""
    try:
        from archon.config import cfg
        if not cfg.groq_api_key:
            return False
        from groq import Groq
        client = Groq(api_key=cfg.groq_api_key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )
        return True
    except Exception:
        return False


# ── Test 1: Full pipeline on fixture repo (mock LLM) ─────────────────────────

def test_full_pipeline_fixture(tmp_path):
    """Runs every phase end-to-end on the sample_repo fixture."""
    from archon.ingestion.ast_parser import parse_repository
    from archon.graph.neo4j_client import make_graph_store, GraphNode, GraphEdge
    from archon.graph.network_graph import ArchonGraph
    from archon.retrieval.bm25 import BM25Index
    from archon.retrieval.vector_store import VectorStore, ContextEngine
    from archon.agent.harness import Harness, HarnessConfig
    from archon.agent.loop import AgentState, build_agent_graph
    from archon.goal_analyzer import GoalAnalyzer
    from archon.verification.hallucination import check_claim, FilterStatus
    from archon.memory.sqlite_store import SQLiteStore
    from archon.docs.generator import DocumentationGenerator

    # ── Phase 1: Parse ───────────────────────────────────────────────────────
    parse_result = parse_repository(FIXTURES)
    assert len(parse_result.modules) >= 4, "Expected ≥4 modules"
    assert len(parse_result.functions) >= 5, "Expected ≥5 functions"
    assert len(parse_result.errors) <= 1, f"Too many parse errors: {parse_result.errors}"

    # ── Phase 2: Graph ───────────────────────────────────────────────────────
    store = make_graph_store(force_inmemory=True)
    for mod in parse_result.modules:
        store.upsert_node(GraphNode(
            id=mod.id, label="Module",
            properties={"path": mod.path, "line_count": mod.line_count},
            confidence=0.9, provenance=f"{mod.id}:1",
        ))
    for fn in parse_result.functions:
        store.upsert_node(GraphNode(
            id=fn.id, label="Function",
            properties={"name": fn.name},
            confidence=0.9, provenance=f"{fn.module_path}:{fn.line_start}",
        ))
    for cls in parse_result.classes:
        store.upsert_node(GraphNode(
            id=cls.id, label="Class",
            properties={"name": cls.name},
            confidence=0.9, provenance=f"{cls.module_path}:{cls.line_start}",
        ))

    nx_graph = ArchonGraph()
    nx_graph.sync_from_store(store)
    assert nx_graph.node_count() >= 4

    # ── Phase 3: Retrieval ───────────────────────────────────────────────────
    chunks = ContextEngine.chunks_from_parse_result(parse_result)
    bm25 = BM25Index()
    bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True)
    vs.add_chunks(chunks)
    engine = ContextEngine(bm25, vs)

    results = engine.query("authentication login password", top_k=5)
    assert len(results) > 0
    auth_ids = [r.id for r in results]
    assert any("auth" in rid.lower() for rid in auth_ids), (
        f"Expected auth chunk in results, got: {auth_ids}"
    )

    # ── Phase 4: Goal analysis (mock LLM) ────────────────────────────────────
    goal = "Understand the authentication module and trace the login flow"
    analyzer = GoalAnalyzer(llm=_MockLLM())
    inv_goal = analyzer.analyze(goal)
    assert len(inv_goal.investigation_tasks) >= 2
    assert len(inv_goal.success_criteria) >= 1

    # ── Phase 5-6: Agent loop (mock LLM, harness) ────────────────────────────
    harness = Harness(HarnessConfig(
        allowed_tools={"ast_analysis", "radon", "ripgrep", "git_log"},
        call_limit_per_tool=5,
    ))
    agent_graph = build_agent_graph(
        llm=_MockLLM(), harness=harness, store=store, max_iterations=6,
        ctx_engine=engine, repo_root=FIXTURES,
    )
    init = AgentState(goal=goal, tasks=inv_goal.investigation_tasks[:2]).model_dump()
    final = agent_graph.invoke(init)

    assert final["complete"] is True
    assert len(final["findings"]) >= 1, "agent produced no grounded findings"

    # ── Phase 6: every finding carries real file:line provenance ─────────────
    import re
    for finding_text in final["findings"]:
        assert re.search(r"\.py:\d+", finding_text), f"ungrounded finding: {finding_text}"
        assert "synthetic" not in finding_text

    # ── Phase 7: Memory ───────────────────────────────────────────────────────
    db = SQLiteStore(db_path=":memory:")
    db.create_session("e2e_sess", goal)
    db.save_iteration("e2e_sess", final)
    loaded = db.load_session("e2e_sess")
    assert len(loaded) == 1

    # ── Phase 8: Documentation ────────────────────────────────────────────────
    gen = DocumentationGenerator(store, parse_result)
    out = gen.generate("e2e_sess", tmp_path, goal=goal)

    report = tmp_path / "report.md"
    assert report.exists()
    content = report.read_text()
    assert "authentication" in content.lower() or "auth" in content.lower()

    module_docs = list((tmp_path / "modules").glob("*.md"))
    assert len(module_docs) >= 4, f"Expected ≥4 module docs, got {len(module_docs)}"

    assert (tmp_path / "architecture.dot").exists()
    assert (tmp_path / "architecture.png").exists()
    assert (tmp_path / "callgraph.dot").exists()

    # ── Eval metrics ─────────────────────────────────────────────────────────
    # Architecture reconstruction: ≥4 modules found (target ≥80% of 5 real modules)
    module_nodes = [n for n in store.all_nodes() if n.label == "Module"]
    assert len(module_nodes) >= 4, f"Architecture recall: {len(module_nodes)}/5"

    # All promoted findings have confidence set (not 0)
    hypothesis_nodes = [n for n in store.all_nodes() if n.label == "Hypothesis"]
    for h in hypothesis_nodes:
        assert h.confidence > 0, f"Hypothesis {h.id} has confidence=0"

    print(f"\n[E2E PASS] modules={len(module_nodes)}, "
          f"findings={len(final['findings'])}, "
          f"module_docs={len(module_docs)}")


# ── Test 2: Real Groq GoalAnalyzer ───────────────────────────────────────────

@pytest.mark.skipif(not _groq_reachable(), reason="api.groq.com not reachable")
def test_groq_goal_analyzer():
    """Calls real Groq API to decompose an investigation goal."""
    from archon.llm import make_llm
    from archon.goal_analyzer import GoalAnalyzer

    llm = make_llm()
    analyzer = GoalAnalyzer(llm=llm)
    goal = analyzer.analyze("Understand the routing system in a Flask web application")

    assert len(goal.investigation_tasks) >= 2, (
        f"Expected ≥2 tasks from Groq, got: {goal.investigation_tasks}"
    )
    assert len(goal.success_criteria) >= 1
    print(f"\n[GROQ] Tasks: {goal.investigation_tasks}")


# ── Test 3: Real Groq hypothesis verification ─────────────────────────────────

@pytest.mark.skipif(not _groq_reachable(), reason="api.groq.com not reachable")
def test_groq_verify():
    """Calls real Groq to verify a hypothesis against source evidence."""
    from archon.llm import make_llm
    from langchain_core.messages import HumanMessage, SystemMessage

    llm = make_llm()
    messages = [
        SystemMessage(content=(
            "You are a code verification engine. "
            "Given a hypothesis and evidence, respond with ONLY one word: "
            "VERIFIED, REFUTED, or UNCERTAIN."
        )),
        HumanMessage(content=(
            "Hypothesis: The auth module contains a function that hashes passwords.\n\n"
            "Evidence:\n"
            "- [auth.py:14] def hash_password(self, password: str) -> str:\n"
            "- [auth.py:15]     salt = os.urandom(16).hex()\n"
            "- [auth.py:16]     hashed = hashlib.sha256((password + salt).encode()).hexdigest()"
        )),
    ]
    resp = llm.invoke(messages)
    verdict = resp.content.strip().upper()
    assert "VERIFIED" in verdict, f"Expected VERIFIED, got: {verdict}"
    print(f"\n[GROQ] Verdict: {verdict}")
