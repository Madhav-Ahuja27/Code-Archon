"""Phase 8 — Documentation Generator tests.

Gate: all 8 pass before Phase 9 begins.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from archon.docs.generator import DocumentationGenerator
from archon.graph.neo4j_client import GraphEdge, GraphNode, make_graph_store
from archon.ingestion.ast_parser import parse_repository

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"


@pytest.fixture
def populated_store():
    """In-memory store with Module, Function, Hypothesis, CALLS edges."""
    store = make_graph_store(force_inmemory=True)
    # Modules
    store.upsert_node(GraphNode(id="auth.py", label="Module",
                                properties={"path": str(FIXTURES / "auth.py"),
                                            "line_count": 30},
                                confidence=0.9, provenance="auth.py:1"))
    store.upsert_node(GraphNode(id="api.py", label="Module",
                                properties={"path": str(FIXTURES / "api.py"),
                                            "line_count": 20},
                                confidence=0.9, provenance="api.py:1"))
    store.upsert_node(GraphNode(id="models.py", label="Module",
                                properties={"path": str(FIXTURES / "models.py"),
                                            "line_count": 25},
                                confidence=0.9, provenance="models.py:1"))
    # Functions
    store.upsert_node(GraphNode(id="auth.py::login", label="Function",
                                properties={"name": "login"},
                                confidence=0.8, provenance="auth.py:10"))
    store.upsert_node(GraphNode(id="auth.py::hash_password", label="Function",
                                properties={"name": "hash_password"},
                                confidence=0.85, provenance="auth.py:14"))
    # CALLS edge
    store.upsert_edge(GraphEdge(source_id="auth.py::login",
                                target_id="auth.py::hash_password",
                                rel_type="CALLS"))
    store.upsert_edge(GraphEdge(source_id="api.py", target_id="auth.py",
                                rel_type="IMPORTS"))
    # Verified findings
    store.upsert_node(GraphNode(id="finding::1", label="Hypothesis",
                                properties={"claim": "auth module handles password hashing"},
                                confidence=0.9, provenance="auth.py:14"))
    store.upsert_node(GraphNode(id="finding::2", label="Hypothesis",
                                properties={"claim": "api.py imports auth"},
                                confidence=0.85, provenance="api.py:3"))
    return store


@pytest.fixture
def parse_result():
    return parse_repository(FIXTURES)


@pytest.fixture
def gen(populated_store, parse_result):
    return DocumentationGenerator(populated_store, parse_result)


# ── Test 1: report.md generated ──────────────────────────────────────────────

def test_report_md_generated(gen, tmp_path):
    gen.generate("sess_001", tmp_path, goal="understand authentication")
    assert (tmp_path / "report.md").exists()


# ── Test 2: report.md contains confidence table ───────────────────────────────

def test_report_has_confidence_table(gen, tmp_path):
    gen.generate("sess_001", tmp_path, goal="understand authentication")
    content = (tmp_path / "report.md").read_text()
    assert "| Confidence |" in content or "Confidence" in content


# ── Test 3: per-module .md files generated ────────────────────────────────────

def test_module_docs_generated(gen, tmp_path, parse_result):
    gen.generate("sess_001", tmp_path)
    module_files = list((tmp_path / "modules").glob("*.md"))
    assert len(module_files) == len(parse_result.modules), (
        f"Expected {len(parse_result.modules)} module docs, got {len(module_files)}"
    )


# ── Test 4: module doc lists function names ───────────────────────────────────

def test_module_doc_has_functions(gen, tmp_path):
    gen.generate("sess_001", tmp_path)
    modules_dir = tmp_path / "modules"
    auth_doc = modules_dir / "auth.py.md"
    assert auth_doc.exists(), f"auth.py.md not found in {list(modules_dir.iterdir())}"
    content = auth_doc.read_text()
    assert "hash_password" in content
    assert "verify_password" in content


# ── Test 5: architecture.dot generated ───────────────────────────────────────

def test_architecture_dot_generated(gen, tmp_path):
    gen.generate("sess_001", tmp_path)
    dot = tmp_path / "architecture.dot"
    assert dot.exists()
    content = dot.read_text()
    assert "digraph" in content


# ── Test 6: architecture.png rendered ────────────────────────────────────────

def test_architecture_png_rendered(gen, tmp_path):
    gen.generate("sess_001", tmp_path)
    png = tmp_path / "architecture.png"
    assert png.exists(), "architecture.png not generated"
    assert png.stat().st_size > 0


# ── Test 7: callgraph.dot and .png generated ─────────────────────────────────

def test_callgraph_generated(gen, tmp_path):
    gen.generate("sess_001", tmp_path)
    assert (tmp_path / "callgraph.dot").exists()
    assert (tmp_path / "callgraph.png").exists()
    content = (tmp_path / "callgraph.dot").read_text()
    assert "digraph" in content


# ── Test 8: empty session (0 verified nodes) → empty report, no crash ────────

def test_empty_session_no_crash(tmp_path):
    store = make_graph_store(force_inmemory=True)
    gen = DocumentationGenerator(store, parse_result=None)
    gen.generate("empty_sess", tmp_path, goal="nothing to find")
    report = tmp_path / "report.md"
    assert report.exists()
    content = report.read_text()
    assert "0" in content or "none" in content.lower() or "All investigation" in content
