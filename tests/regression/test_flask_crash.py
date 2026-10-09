"""Regression: duplicate IDs crashed ChromaDB and silently merged graph nodes
when one file defines the same name several times (seen on Flask 1.1.4 tests)."""

import textwrap
from pathlib import Path

from archon.graph.builder import build_graph
from archon.graph.neo4j_client import make_graph_store
from archon.ingestion.ast_parser import parse_repository
from archon.retrieval.bm25 import BM25Index
from archon.retrieval.vector_store import ContextEngine, VectorStore

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"


def _repo(tmp_path):
    (tmp_path / "t.py").write_text(textwrap.dedent("""
        def test_a():
            def index(): pass
        def test_b():
            def index(): pass
        def handler(): pass
        def handler(): pass          # redefinition at module level
        class Enc: pass
        def test_c():
            class Enc: pass          # same class name, different scope
    """), encoding="utf-8")
    return tmp_path


def test_all_ids_unique(tmp_path):
    r = parse_repository(_repo(tmp_path))
    ids = [f.id for f in r.functions] + [c.id for c in r.classes]
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"


def test_no_nodes_lost_in_graph(tmp_path):
    r = parse_repository(_repo(tmp_path))
    store = make_graph_store(force_inmemory=True)
    build_graph(r, store)
    expected = len(r.modules) + len(r.functions) + len(r.classes)
    assert store.node_count() == expected


def test_chroma_accepts_all_chunks(tmp_path):
    r = parse_repository(_repo(tmp_path))
    chunks = ContextEngine.chunks_from_parse_result(r)
    vs = VectorStore(use_hash_embed=True)
    vs.add_chunks(chunks)           # used to raise DuplicateIDError
    assert vs.count() == len(chunks)


def test_large_batch_upsert():
    from archon.retrieval.bm25 import Chunk
    chunks = [Chunk(id=f"m::f{i}", text=f"fn {i}", file_path="m.py") for i in range(1700)]
    vs = VectorStore(use_hash_embed=True)
    vs.add_chunks(chunks)
    assert vs.count() == 1700


def test_ids_use_forward_slashes(tmp_path):
    pkg = tmp_path / "pkg" / "sub"
    pkg.mkdir(parents=True)
    (pkg / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    r = parse_repository(tmp_path)
    assert r.modules[0].id == "pkg/sub/m.py"
    assert "\\" not in r.functions[0].id


# ── graph builder edges ──────────────────────────────────────────────────────

def _edges(rel):
    r = parse_repository(FIXTURES)
    store = make_graph_store(force_inmemory=True)
    build_graph(r, store)
    return {(e.source_id, e.target_id) for e in store.edges_by_type(rel)}


def test_imports_edges():
    e = _edges("IMPORTS")
    assert ("api.py", "auth.py") in e
    assert ("api.py", "models.py") in e


def test_inherits_edges():
    e = _edges("INHERITS")
    assert ("models.py::User", "models.py::Base") in e
    assert ("models.py::AdminUser", "models.py::User") in e


def test_calls_edges():
    e = _edges("CALLS")
    assert ("api.py::login", "auth.py::create_auth") in e
    assert ("api.py::login", "auth.py::UserAuth::hash_password") in e


def test_contains_edges():
    e = _edges("CONTAINS")
    assert ("auth.py", "auth.py::UserAuth") in e
    assert ("auth.py", "auth.py::create_auth") in e


def test_noise_names_not_linked_across_modules(tmp_path):
    (tmp_path / "a.py").write_text("def get(): pass\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("def use(d):\n    return d.get('x')\n", encoding="utf-8")
    r = parse_repository(tmp_path)
    store = make_graph_store(force_inmemory=True)
    build_graph(r, store)
    assert store.edges_by_type("CALLS") == []


def test_ambiguous_calls_skipped(tmp_path):
    (tmp_path / "a.py").write_text("def helper(): pass\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("def helper(): pass\n", encoding="utf-8")
    (tmp_path / "c.py").write_text("def use():\n    helper()\n", encoding="utf-8")
    r = parse_repository(tmp_path)
    store = make_graph_store(force_inmemory=True)
    build_graph(r, store)
    assert store.edges_by_type("CALLS") == []


def test_sqlite_creates_missing_parent_dir(tmp_path):
    from archon.memory.sqlite_store import SQLiteStore
    db = SQLiteStore(tmp_path / "does" / "not" / "exist" / "session.db")
    db.create_session("s", "g")
    assert db.session_exists("s")
    db.close()


# ── ChromaDB native engine missing (Windows "DLL load failed") ──────────────

def _break_chroma(monkeypatch):
    import chromadb

    def boom(*a, **k):
        raise ImportError("DLL load failed while importing chromadb_rust_bindings")

    monkeypatch.setattr(chromadb, "EphemeralClient", boom)
    monkeypatch.setattr(chromadb, "PersistentClient", boom)


def test_vector_store_survives_broken_chromadb(monkeypatch):
    from archon.retrieval.bm25 import Chunk
    _break_chroma(monkeypatch)
    vs = VectorStore(use_hash_embed=True)
    assert vs.backend == "builtin"
    vs.add_chunks([Chunk(id=f"m::f{i}", text=f"word{i}", file_path="m.py") for i in range(1700)])
    assert vs.count() == 1700
    vs.clear()
    assert vs.count() == 0 and vs.query("x") == []


def test_builtin_index_ranks_by_shared_vocabulary(monkeypatch):
    from archon.retrieval.bm25 import Chunk
    _break_chroma(monkeypatch)
    vs = VectorStore(use_hash_embed=True)
    vs.add_chunks([
        Chunk(id="auth", text="def hash_password verify password login", file_path="auth.py", line_start=3),
        Chunk(id="db", text="def connect database cursor query", file_path="db.py", line_start=9),
    ])
    top = vs.query("password hashing", top_k=2)
    assert top[0].id == "auth" and top[0].file_path == "auth.py" and top[0].line_start == 3
    assert 0.0 <= top[1].score <= top[0].score <= 1.0


def test_full_pipeline_works_without_chromadb(monkeypatch, tmp_path):
    """Agent + evidence + gate run end to end on the built-in index."""
    from archon.agent.harness import Harness, HarnessConfig
    from archon.agent.loop import AgentState, build_agent_graph
    _break_chroma(monkeypatch)
    pr = parse_repository(FIXTURES)
    store = make_graph_store(force_inmemory=True)
    build_graph(pr, store)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    g = build_agent_graph(harness=Harness(HarnessConfig(allowed_tools={"ripgrep"})),
                          store=store, max_iterations=4,
                          ctx_engine=ContextEngine(bm25, vs), repo_root=FIXTURES)
    final = g.invoke(AgentState(goal="g", tasks=["authentication password hashing"]).model_dump())
    assert vs.backend == "builtin" and len(final["findings"]) == 1


def test_lexical_embedding_properties():
    from archon.retrieval.vector_store import _lexical_embed
    a, b, c = (_lexical_embed(t) for t in ("hash password", "password hashing helper", "database cursor"))
    dot = lambda x, y: sum(i * j for i, j in zip(x, y))
    assert abs(dot(a, a) - 1.0) < 1e-9
    assert dot(a, b) > dot(a, c)                       # shared word beats unrelated
    assert _lexical_embed("camelCaseName") == _lexical_embed("camel case name")
