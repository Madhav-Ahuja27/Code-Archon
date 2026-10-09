import json, re
from pathlib import Path
from archon.agent.harness import Harness, HarnessConfig
from archon.agent.loop import AgentState, build_agent_graph
from archon.graph.builder import build_graph
from archon.graph.neo4j_client import make_graph_store
from archon.ingestion.ast_parser import parse_repository
from archon.retrieval.bm25 import BM25Index
from archon.retrieval.vector_store import ContextEngine, VectorStore
from archon.ui_export import build_ui, _snippet

FIX = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"


def _run(tmp_path):
    pr = parse_repository(FIX); store = make_graph_store(force_inmemory=True); build_graph(pr, store)
    ch = ContextEngine.chunks_from_parse_result(pr); b = BM25Index(); b.build(ch)
    v = VectorStore(use_hash_embed=True); v.add_chunks(ch)
    g = build_agent_graph(harness=Harness(HarnessConfig(allowed_tools={"ripgrep"})), store=store,
                          max_iterations=6, ctx_engine=ContextEngine(b, v), repo_root=FIX)
    final = g.invoke(AgentState(goal="g", tasks=["authentication password hashing", "zebra quantum"]).model_dump())
    out = build_ui(store, pr, final, FIX, "understand auth", "s1", "heuristic", tmp_path / "index.html")
    return out.read_text(encoding="utf-8")


def _data(html):
    m = re.search(r"const D=(\{.*?\}),\$=s=>", html, re.S)
    return json.loads(m.group(1))


def test_dashboard_embeds_findings_graph_and_source(tmp_path):
    d = _data(_run(tmp_path))
    assert d["stats"]["findings"] == 1 and d["unknowns"] == ["zebra quantum"]
    f = d["findings"][0]
    assert f["evidence"] and f["provenance"] in d["sources"]
    src = d["sources"][f["provenance"]]
    assert src["lines"] and src["hl"] >= src["start"]
    assert any(n["cited"] for n in d["graph"]["nodes"])
    assert d["graph"]["edges"]


def test_dashboard_is_self_contained_and_script_safe(tmp_path):
    html = _run(tmp_path)
    assert "cytoscape" in html and "http://" not in html.split("<script>")[2][:2000]
    assert "/*__DATA__*/" not in html and "/*__CYTOSCAPE__*/" not in html


def test_snippet_blocks_path_traversal():
    assert _snippet(FIX, "../../pyproject.toml:1") is None
    assert _snippet(FIX, "auth.py:5") is not None
    assert _snippet(FIX, "missing.py:1") is None


def test_dashboard_surfaces_backend_and_output_sections(tmp_path):
    html = _run(tmp_path)
    d = _data(html)
    assert "Agent journey" in html
    assert "Evidence lab" in html
    assert "Knowledge graph" in html
    assert "Codebase explorer" in html
    assert "Generated artefacts" in html
    assert {"modules", "functions", "classes"} <= d.keys()
    assert {"agent", "history", "evidence", "artifacts", "tasks"} <= d.keys()
    assert "tool_calls" in d["agent"]
    assert isinstance(d["graph"]["edges"], list)
