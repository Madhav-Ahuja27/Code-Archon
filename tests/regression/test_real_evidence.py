"""The agent must work from real evidence and the provenance gate must be enforced."""

import re
from pathlib import Path

import pytest

from archon.agent.evidence import extract_keywords, gather_evidence, is_source_path
from archon.agent.harness import Harness, HarnessConfig
from archon.agent.loop import AgentState, build_agent_graph
from archon.graph.builder import build_graph
from archon.graph.neo4j_client import make_graph_store
from archon.ingestion.ast_parser import parse_repository
from archon.retrieval.bm25 import BM25Index
from archon.retrieval.vector_store import ContextEngine, VectorStore
from archon.verification.hallucination import FilterStatus, check_claim_grounded

FIX = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"
PROV = re.compile(r"\.py:\d+")


def _setup():
    pr = parse_repository(FIX)
    store = make_graph_store(force_inmemory=True)
    build_graph(pr, store)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    return store, ContextEngine(bm25, vs)


def _harness(limit=5):
    return Harness(HarnessConfig(allowed_tools={"ripgrep"}, call_limit_per_tool=limit))


class _Resp:
    def __init__(self, c): self.content = c


class CitingLLM:
    """Cites a real source taken from the evidence it is shown."""
    def invoke(self, messages):
        system, human = str(messages[0].content), str(messages[-1].content)
        if "code archaeologist" in system:
            m = re.search(r"\[([\w/.\\-]+\.py:\d+)\]", human)
            return _Resp(f"Handled in {m.group(1)}." if m else "INSUFFICIENT")
        return _Resp("VERIFIED")


class FabricatingLLM:
    """Cites a file that does not exist in the evidence."""
    def invoke(self, messages):
        if "code archaeologist" in str(messages[0].content):
            return _Resp("Routing is done in ghost/router.py:99.")
        return _Resp("VERIFIED")


# ── evidence ────────────────────────────────────────────────────────────────

def test_gather_evidence_all_items_have_provenance():
    store, engine = _setup()
    ev = gather_evidence("authentication password hashing", engine, FIX, _harness(), store)
    assert len(ev) > 0
    assert all(PROV.search(e.source) for e in ev), [e.source for e in ev]
    assert {e.tool for e in ev} & {"retrieval", "ripgrep"}


def test_gather_evidence_uses_graph_neighbours():
    store, engine = _setup()
    ev = gather_evidence("login password hashing", engine, FIX, _harness(), store)
    assert any(e.tool == "graph" for e in ev)


def test_keywords_skip_generic_words():
    kws = extract_keywords("Locate and review routing configuration files", n=3)
    assert "routing" in kws and "locate" not in kws and "files" not in kws


@pytest.mark.parametrize("path,expected", [
    ("src/flask/app.py", True), ("tests/test_basic.py", False),
    ("docs/conf.py", False), ("examples/x/app.py", False),
    ("pkg/tests/helpers.py", False), ("pkg/test_x.py", False),
])
def test_is_source_path(path, expected):
    assert is_source_path(path) is expected


# ── gate ────────────────────────────────────────────────────────────────────

EV = [("auth.py:14", "def hash_password"), ("api.py:5", "def login")]


def test_gate_passes_grounded_citation():
    r = check_claim_grounded("Hashing is in auth.py:14.", EV, require_citation=True)
    assert r.status == FilterStatus.PASSES and "auth.py:14" in r.provenance_found


def test_gate_accepts_path_prefix_difference():
    r = check_claim_grounded("See src/pkg/auth.py:14.", EV, require_citation=True)
    assert r.status == FilterStatus.PASSES


def test_gate_blocks_fabricated_file():
    r = check_claim_grounded("It lives in ghost/router.py:99.", EV, require_citation=True)
    assert r.status == FilterStatus.HALLUCINATED


def test_gate_blocks_mixed_real_and_fake_citations():
    r = check_claim_grounded("See auth.py:14 and ghost.py:1.", EV)
    assert r.status == FilterStatus.HALLUCINATED


def test_gate_requires_citation_in_llm_mode_only():
    assert check_claim_grounded("no citation", EV, require_citation=True).status == FilterStatus.HALLUCINATED
    assert check_claim_grounded("no citation", EV, require_citation=False).status == FilterStatus.PASSES


def test_gate_blocks_evidence_without_provenance():
    r = check_claim_grounded("anything", [("synthetic:iter_1", "Analyzed goal")])
    assert r.status == FilterStatus.HALLUCINATED


# ── full loop ───────────────────────────────────────────────────────────────

def _run(llm, tasks, max_iter=8, limit=5):
    store, engine = _setup()
    h = _harness(limit)
    g = build_agent_graph(llm=llm, harness=h, store=store, max_iterations=max_iter,
                          ctx_engine=engine, repo_root=FIX)
    final = g.invoke(AgentState(goal="g", tasks=tasks).model_dump())
    return final, store, h


def test_llm_grounded_claims_become_findings_and_graph_nodes():
    final, store, _ = _run(CitingLLM(), ["authentication password hashing", "login flow"])
    assert final["complete"] and final["task_index"] == 2
    assert len(final["findings"]) == 2 and final["unknowns"] == []
    assert all(PROV.search(f) for f in final["findings"])
    hyp = [n for n in store.all_nodes() if n.label == "Hypothesis"]
    assert len(hyp) == 2 and all(PROV.search(n.provenance) for n in hyp)
    assert any(n.label == "Evidence" for n in store.all_nodes())
    assert store.edges_by_type("SUPPORTS") and store.edges_by_type("ABOUT")


def test_fabricated_claims_are_blocked_and_reported_unresolved():
    final, store, _ = _run(FabricatingLLM(), ["authentication password hashing"], max_iter=8)
    assert final["findings"] == []
    assert len(final["rejected"]) >= 1
    assert "authentication password hashing" in final["unknowns"]
    assert [n for n in store.all_nodes() if n.label == "Hypothesis"] == []


def test_heuristic_mode_without_llm_still_grounded():
    final, store, _ = _run(None, ["authentication password hashing"])
    assert len(final["findings"]) == 1 and PROV.search(final["findings"][0])


def test_irrelevant_task_is_unresolved_not_fake_verified():
    final, _, _ = _run(None, ["quantum chromodynamics zebra"], max_iter=8)
    assert final["findings"] == []
    assert final["unknowns"] == ["quantum chromodynamics zebra"]


def test_tool_budget_is_per_iteration_not_global():
    final, _, h = _run(CitingLLM(), ["auth password", "login flow", "models user", "api routes"],
                       max_iter=10, limit=2)
    assert final["complete"] and final["task_index"] == 4
    assert len(h.call_log()) > 2          # more calls than one iteration's budget


def test_budget_exhaustion_marks_remaining_tasks_unresolved():
    final, _, _ = _run(CitingLLM(), ["authentication password", "login flow", "models user"],
                       max_iter=1)
    assert final["complete"]
    assert len(final["findings"]) == 1
    assert len(final["unknowns"]) == 2


def test_retry_counter_resets_between_tasks():
    final, _, _ = _run(None, ["quantum zebra", "authentication password hashing"], max_iter=10)
    assert final["unknowns"] == ["quantum zebra"]
    assert len(final["findings"]) == 1


# ── Neo4j (runs only when Docker Neo4j is up) ───────────────────────────────

def test_neo4j_all_nodes_includes_hypothesis():
    from archon.graph.neo4j_client import GraphNode, _Neo4jStore
    store = make_graph_store()
    if not isinstance(store, _Neo4jStore):
        pytest.skip("Neo4j not running")
    try:
        store.upsert_node(GraphNode(id="pytest::finding", label="Hypothesis",
                                    properties={"claim": "c"}, confidence=0.9,
                                    provenance="a.py:1"))
        assert "pytest::finding" in {n.id for n in store.all_nodes()}
    finally:
        with store._driver.session() as s:
            s.run("MATCH (n) WHERE n.id STARTS WITH 'pytest::' DETACH DELETE n")


# ── Neo4j startup wait ──────────────────────────────────────────────────────

def test_waits_for_neo4j_that_is_still_booting(monkeypatch):
    from archon.graph import neo4j_client as nc
    attempts = {"n": 0}

    class _Driver:
        def verify_connectivity(self):
            if attempts["n"] < 3:
                raise ConnectionError("incomplete handshake")

    class _Fake:
        def __init__(self, *a, **k):
            attempts["n"] += 1
            self._driver = _Driver()

    monkeypatch.setattr(nc, "_Neo4jStore", _Fake)
    monkeypatch.setattr(nc, "_port_open", lambda *a, **k: True)
    monkeypatch.setattr("time.sleep", lambda s: None)
    store = nc.make_graph_store(wait=30)
    assert isinstance(store, _Fake) and attempts["n"] == 3


def test_no_wait_when_nothing_is_listening(monkeypatch):
    from archon.graph import neo4j_client as nc
    attempts = {"n": 0}

    class _Fake:
        def __init__(self, *a, **k):
            attempts["n"] += 1
            raise ConnectionError("refused")

    monkeypatch.setattr(nc, "_Neo4jStore", _Fake)
    monkeypatch.setattr(nc, "_port_open", lambda *a, **k: False)
    store = nc.make_graph_store(wait=30)
    assert isinstance(store, nc._InMemoryStore) and attempts["n"] == 1


def test_wait_zero_falls_back_immediately(monkeypatch):
    from archon.graph import neo4j_client as nc

    class _Fake:
        def __init__(self, *a, **k): raise ConnectionError("not ready")

    monkeypatch.setattr(nc, "_Neo4jStore", _Fake)
    monkeypatch.setattr(nc, "_port_open", lambda *a, **k: True)
    assert isinstance(nc.make_graph_store(wait=0), nc._InMemoryStore)


# ── gate is line-level ──────────────────────────────────────────────────────

def test_gate_blocks_right_file_wrong_line():
    r = check_claim_grounded("Hashing is in auth.py:99.", EV, require_citation=True)
    assert r.status == FilterStatus.HALLUCINATED


def test_gate_accepts_right_file_right_line_with_prefix():
    r = check_claim_grounded("See src/pkg/auth.py:14 and api.py:5.", EV)
    assert r.status == FilterStatus.PASSES


# ── evidence quality ────────────────────────────────────────────────────────

def _ripgrep_evidence(tmp_path, files, task):
    for name, body in files.items():
        (tmp_path / name).write_text(body, encoding="utf-8")
    pr = parse_repository(tmp_path)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    ev = gather_evidence(task, ContextEngine(bm25, vs), tmp_path)
    return [e for e in ev if e.tool == "ripgrep"]


def test_imports_and_comments_are_not_evidence(tmp_path):
    ev = _ripgrep_evidence(tmp_path, {
        "m.py": "from werkzeug.routing import Rule\nimport routing_utils\n"
                "# the routing table\ndef add_routing(x):\n    return x\n",
    }, "routing table")
    lines = {int(e.source.rsplit(":", 1)[1]) for e in ev}
    assert 4 in lines and not (lines & {1, 2, 3})


def test_definitions_outrank_plain_usages_and_file_order(tmp_path):
    usages = "\n".join(f"x{i} = route_table[{i}]" for i in range(12))
    ev = _ripgrep_evidence(tmp_path, {
        "a_first.py": usages + "\n",
        "z_last.py": "def route_handler():\n    pass\n",
    }, "route handling")
    assert any(e.source == "z_last.py:1" for e in ev), [e.source for e in ev]
    assert ev[0].source == "z_last.py:1"


# ── ripgrep tool robustness (the bugs seen on Windows) ──────────────────────

def test_rg_path_does_not_log_errors(tmp_path, caplog):
    import shutil
    if not shutil.which("rg"):
        pytest.skip("rg not installed")
    from archon.tools.search import ripgrep
    (tmp_path / "a.py").write_text("def route(): pass\n", encoding="utf-8")
    with caplog.at_level("WARNING"):
        out = ripgrep("route", tmp_path)
    assert len(out) == 1 and not [r for r in caplog.records if "ripgrep error" in r.getMessage()]


def test_subprocess_decoded_as_utf8_not_platform_default(monkeypatch, tmp_path):
    import subprocess
    from archon.tools import search
    seen = {}

    def fake_run(cmd, **kw):
        seen.update(kw)
        return subprocess.CompletedProcess(cmd, 1, stdout=None, stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert search.ripgrep("x", tmp_path) == []          # stdout=None must not crash
    assert seen.get("encoding") == "utf-8" and "text" not in seen


def test_non_ascii_source_is_searchable(tmp_path):
    from archon.tools.search import ripgrep
    (tmp_path / "u.py").write_text("# naïve café ✓ \u2019\ndef route(): pass\n", encoding="utf-8")
    assert any("route" in m.text for m in ripgrep("route", tmp_path))


def test_graphviz_found_outside_path(monkeypatch, tmp_path):
    import shutil
    from archon.docs.generator import find_graphviz_bin
    bindir = tmp_path / "Graphviz 14" / "bin"
    bindir.mkdir(parents=True)
    (bindir / "dot.exe").write_text("")
    monkeypatch.setattr(shutil, "which", lambda *_: None)
    assert find_graphviz_bin([str(tmp_path / "Graphviz*" / "bin")]) == str(bindir)
    assert find_graphviz_bin([str(tmp_path / "Nope*" / "bin")]) is None


# ── strict line-level gate ──────────────────────────────────────────────────

def test_gate_blocks_real_file_but_unseen_line():
    r = check_claim_grounded("Hashing is in auth.py:99.", EV, require_citation=True)
    assert r.status == FilterStatus.HALLUCINATED


def test_gate_accepts_exact_line_with_range_suffix():
    r = check_claim_grounded("See auth.py:14-20 for hashing.", EV, require_citation=True)
    assert r.status == FilterStatus.PASSES


# ── evidence ranking ────────────────────────────────────────────────────────

def test_ripgrep_evidence_prefers_definitions_over_imports(tmp_path):
    (tmp_path / "a.py").write_text(
        "from werkzeug.routing import Rule\n"
        "# routing notes\n"
        "x = routing_table\n"
        "def routing_table():\n    pass\n", encoding="utf-8")
    pr = parse_repository(tmp_path)
    store = make_graph_store(force_inmemory=True); build_graph(pr, store)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    ev = gather_evidence("routing table", ContextEngine(bm25, vs), tmp_path, _harness(), store)
    rg = [e for e in ev if e.tool == "ripgrep"]
    assert rg, "expected ripgrep evidence"
    assert rg[0].content.startswith("def routing_table")      # definition ranked first
    assert not any(e.content.startswith(("from ", "import ", "#")) for e in rg)


# ── ripgrep / subprocess regressions seen on Windows ────────────────────────

def test_rg_binary_path_does_not_crash(caplog):
    import shutil
    from archon.tools.search import ripgrep
    if not shutil.which("rg"):
        pytest.skip("rg not installed")
    with caplog.at_level("WARNING"):
        m = ripgrep("Authentication", FIX)
    assert len(m) > 0
    assert "ripgrep error" not in caplog.text      # used to crash on the rg path


def test_subprocess_calls_decode_utf8_explicitly(monkeypatch):
    import subprocess
    from archon.tools import search
    seen = {}

    class _R:
        returncode = 0
        stdout = "a.py:1:Authentication\n"
        stderr = ""

    def fake_run(cmd, **kw):
        seen.update(kw)
        return _R()

    monkeypatch.setattr(subprocess, "run", fake_run)
    search.ripgrep("Authentication", FIX)
    assert seen.get("encoding") == "utf-8" and "text" not in seen


def test_no_tool_uses_platform_default_text_decoding():
    root = Path(__file__).parent.parent.parent / "archon" / "tools"
    offenders = [f.name for f in root.glob("*.py") if "text=True" in f.read_text(encoding="utf-8")]
    assert offenders == [], f"text=True decodes with cp1252 on Windows: {offenders}"


def test_ripgrep_survives_non_utf8_bytes(tmp_path):
    from archon.tools.search import ripgrep
    (tmp_path / "x.py").write_bytes(b"# caf\xc3\xa9 \x81\x8d\nAuthentication = 1\n")
    m = ripgrep("Authentication", tmp_path)
    assert len(m) == 1 and m[0].line == 2


# ── Graphviz discovery ──────────────────────────────────────────────────────

def test_find_graphviz_bin_searches_install_dirs(tmp_path, monkeypatch):
    import shutil
    from archon.docs.generator import find_graphviz_bin
    monkeypatch.setattr(shutil, "which", lambda *_: None)
    bindir = tmp_path / "Graphviz 12" / "bin"
    bindir.mkdir(parents=True)
    (bindir / "dot.exe").write_text("")
    assert find_graphviz_bin([str(tmp_path / "Graphviz*" / "bin")]) == str(bindir)
    assert find_graphviz_bin([str(tmp_path / "nothing*" / "bin")]) is None


def test_retrieval_evidence_not_crowded_out_by_tests(tmp_path):
    (tmp_path / "tests").mkdir()
    body = "".join(
        f'def test_routing_case_{i}():\n    """routing table routing check {i}"""\n    pass\n\n'
        for i in range(25))
    (tmp_path / "tests" / "test_routes.py").write_text(body, encoding="utf-8")
    (tmp_path / "lib.py").write_text(
        'def build_routing_table():\n    """Build the routing table."""\n    pass\n', encoding="utf-8")
    pr = parse_repository(tmp_path)
    store = make_graph_store(force_inmemory=True); build_graph(pr, store)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    ev = gather_evidence("routing table", ContextEngine(bm25, vs), tmp_path, _harness(), store)
    retrieval = [e for e in ev if e.tool == "retrieval"]
    assert any(e.source.startswith("lib.py:") for e in retrieval), [e.source for e in retrieval]
    assert not any(e.source.startswith("tests/") for e in retrieval)
