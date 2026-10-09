"""Phase 2 — Context Graph (Neo4j + NetworkX) tests.

Uses the in-memory store so no Docker needed.
Gate: all 13 pass before Phase 3 begins.
"""

from __future__ import annotations

import pytest

from archon.graph.neo4j_client import GraphEdge, GraphNode, make_graph_store
from archon.graph.network_graph import ArchonGraph
from archon.ingestion.ast_parser import FunctionNode, ModuleNode, ClassNode


@pytest.fixture
def store():
    """Fresh in-memory graph store for each test."""
    s = make_graph_store(force_inmemory=True)
    yield s
    s.clear()


@pytest.fixture
def graph():
    return ArchonGraph()


# ── helpers ───────────────────────────────────────────────────────────────────

def _module_node(mid: str) -> GraphNode:
    return GraphNode(id=mid, label="Module", properties={"path": mid})


def _fn_node(fid: str, name: str = "fn") -> GraphNode:
    return GraphNode(id=fid, label="Function", properties={"name": name})


def _class_node(cid: str, name: str = "Cls") -> GraphNode:
    return GraphNode(id=cid, label="Class", properties={"name": name})


# ── Test 1 ────────────────────────────────────────────────────────────────────

def test_ingest_module_nodes(store):
    for i in range(3):
        store.upsert_node(_module_node(f"mod{i}.py"))
    modules = store.nodes_by_label("Module")
    assert len(modules) == 3
    ids = {m.id for m in modules}
    assert {"mod0.py", "mod1.py", "mod2.py"} == ids


# ── Test 2 ────────────────────────────────────────────────────────────────────

def test_ingest_function_nodes(store):
    node = GraphNode(
        id="auth.py::UserAuth::hash_password",
        label="Function",
        properties={"name": "hash_password", "module_path": "auth.py"},
        confidence=0.5,
        provenance="auth.py:14",
    )
    store.upsert_node(node)
    retrieved = store.get_node("auth.py::UserAuth::hash_password")
    assert retrieved is not None
    assert retrieved.label == "Function"
    assert retrieved.properties["name"] == "hash_password"
    assert retrieved.provenance == "auth.py:14"


# ── Test 3 ────────────────────────────────────────────────────────────────────

def test_creates_calls_edge(store):
    store.upsert_node(_fn_node("mod::login", "login"))
    store.upsert_node(_fn_node("mod::hash_password", "hash_password"))
    store.upsert_edge(GraphEdge(
        source_id="mod::login",
        target_id="mod::hash_password",
        rel_type="CALLS",
    ))
    edges = store.edges_by_type("CALLS")
    assert len(edges) == 1
    assert edges[0].source_id == "mod::login"
    assert edges[0].target_id == "mod::hash_password"


# ── Test 4 ────────────────────────────────────────────────────────────────────

def test_creates_imports_edge(store):
    store.upsert_node(_module_node("api.py"))
    store.upsert_node(_module_node("auth.py"))
    store.upsert_edge(GraphEdge(
        source_id="api.py", target_id="auth.py", rel_type="IMPORTS"
    ))
    edges = store.edges_by_type("IMPORTS")
    assert any(e.source_id == "api.py" and e.target_id == "auth.py" for e in edges)


# ── Test 5 ────────────────────────────────────────────────────────────────────

def test_creates_inherits_edge(store):
    store.upsert_node(_class_node("mod::Base", "Base"))
    store.upsert_node(_class_node("mod::User", "User"))
    store.upsert_edge(GraphEdge(
        source_id="mod::User", target_id="mod::Base", rel_type="INHERITS"
    ))
    edges = store.edges_by_type("INHERITS")
    assert len(edges) == 1
    assert edges[0].source_id == "mod::User"


# ── Test 6 ────────────────────────────────────────────────────────────────────

def test_confidence_default(store):
    store.upsert_node(_fn_node("mod::fn"))
    node = store.get_node("mod::fn")
    assert node.confidence == 0.5


# ── Test 7 ────────────────────────────────────────────────────────────────────

def test_upsert_updates_confidence(store):
    store.upsert_node(_fn_node("mod::fn"))
    updated = GraphNode(id="mod::fn", label="Function",
                        properties={"name": "fn"}, confidence=0.9)
    store.upsert_node(updated)
    node = store.get_node("mod::fn")
    assert node.confidence == 0.9


# ── Test 8 ────────────────────────────────────────────────────────────────────

def test_find_entry_points(store, graph):
    """A module with no incoming edges is an entry point."""
    store.upsert_node(_module_node("main.py"))
    store.upsert_node(_module_node("utils.py"))
    # main imports utils → utils has an incoming edge, main does not
    store.upsert_edge(GraphEdge(
        source_id="main.py", target_id="utils.py", rel_type="IMPORTS"
    ))
    graph.sync_from_store(store)
    entry_points = graph.find_entry_points()
    assert "main.py" in entry_points
    assert "utils.py" not in entry_points


# ── Test 9 ────────────────────────────────────────────────────────────────────

def test_find_dead_code(store, graph):
    """A Function node never targeted by CALLS is dead code."""
    store.upsert_node(_fn_node("mod::login", "login"))
    store.upsert_node(_fn_node("mod::unused", "unused"))
    store.upsert_edge(GraphEdge(
        source_id="mod::login", target_id="mod::login", rel_type="CALLS"
    ))
    graph.sync_from_store(store)
    dead = graph.find_dead_code()
    assert "mod::unused" in dead
    # login calls itself so it IS in the called set
    assert "mod::login" not in dead


# ── Test 10 ───────────────────────────────────────────────────────────────────

def test_get_call_chain(store, graph):
    """BFS call chain A→B→C returns all three nodes."""
    a, b, c = "mod::A", "mod::B", "mod::C"
    for nid in [a, b, c]:
        store.upsert_node(GraphNode(id=nid, label="Function",
                                    properties={"name": nid.split("::")[-1]}))
    store.upsert_edge(GraphEdge(source_id=a, target_id=b, rel_type="CALLS"))
    store.upsert_edge(GraphEdge(source_id=b, target_id=c, rel_type="CALLS"))
    graph.sync_from_store(store)
    chain = graph.get_call_chain(a)
    assert a in chain
    assert b in chain
    assert c in chain


# ── Test 11 ───────────────────────────────────────────────────────────────────

def test_networkx_cycle_detection(store, graph):
    """A→B→A creates a cycle that must be detected."""
    a, b = "mod::A", "mod::B"
    store.upsert_node(_fn_node(a, "A"))
    store.upsert_node(_fn_node(b, "B"))
    store.upsert_edge(GraphEdge(source_id=a, target_id=b, rel_type="CALLS"))
    store.upsert_edge(GraphEdge(source_id=b, target_id=a, rel_type="CALLS"))
    graph.sync_from_store(store)
    assert graph.has_cycle() is True
    cycles = graph.find_cycles()
    assert len(cycles) >= 1


# ── Test 12 ───────────────────────────────────────────────────────────────────

def test_low_confidence_query(store):
    """Nodes below threshold must all be returned."""
    store.upsert_node(GraphNode(id="lo1", label="Function",
                                properties={}, confidence=0.2))
    store.upsert_node(GraphNode(id="lo2", label="Function",
                                properties={}, confidence=0.3))
    store.upsert_node(GraphNode(id="hi1", label="Function",
                                properties={}, confidence=0.8))
    low = store.low_confidence_nodes(threshold=0.5)
    ids = {n.id for n in low}
    assert "lo1" in ids
    assert "lo2" in ids
    assert "hi1" not in ids


# ── Test 13 ───────────────────────────────────────────────────────────────────

def test_clear_graph(store):
    store.upsert_node(_module_node("a.py"))
    store.upsert_node(_module_node("b.py"))
    assert store.node_count() == 2
    store.clear()
    assert store.node_count() == 0
