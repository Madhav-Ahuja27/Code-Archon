"""NetworkX in-process graph mirror.

Fast traversal: cycle detection, BFS call chains, entry points, dead code.
Syncs from the graph store (Neo4j or in-memory).
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:
    from archon.graph.neo4j_client import _InMemoryStore, _Neo4jStore

log = logging.getLogger(__name__)


class ArchonGraph:
    """Directed multigraph with analysis helpers."""

    def __init__(self):
        self._g: nx.DiGraph = nx.DiGraph()

    # ── Mutation ──────────────────────────────────────────────────────────────

    def add_node(self, node_id: str, **attrs) -> None:
        self._g.add_node(node_id, **attrs)

    def add_edge(self, source: str, target: str, rel_type: str, **attrs) -> None:
        self._g.add_edge(source, target, rel_type=rel_type, **attrs)

    def remove_node(self, node_id: str) -> None:
        self._g.remove_node(node_id)

    def clear(self) -> None:
        self._g.clear()

    # ── Sync from store ───────────────────────────────────────────────────────

    def sync_from_store(self, store) -> None:
        """Rebuild NetworkX graph from a graph store snapshot."""
        self.clear()
        for node in store.all_nodes():
            self._g.add_node(node.id, label=node.label,
                             confidence=node.confidence, **node.properties)
        for edge in store.all_edges():
            self._g.add_edge(edge.source_id, edge.target_id,
                             rel_type=edge.rel_type, **edge.properties)

    # ── Queries ───────────────────────────────────────────────────────────────

    def find_entry_points(self) -> list[str]:
        """Nodes with no incoming edges (nothing calls/imports them)."""
        return [n for n in self._g.nodes if self._g.in_degree(n) == 0]

    def find_dead_code(self, rel_type: str = "CALLS") -> list[str]:
        """Function nodes never targeted by a CALLS edge."""
        called = {e[1] for e in self._g.edges if
                  self._g.edges[e].get("rel_type") == rel_type}
        fn_nodes = [n for n, d in self._g.nodes(data=True)
                    if d.get("label") == "Function"]
        return [n for n in fn_nodes if n not in called]

    def get_call_chain(self, start: str) -> list[str]:
        """BFS from start following CALLS edges. Returns all reachable nodes."""
        call_graph = nx.DiGraph(
            (u, v) for u, v, d in self._g.edges(data=True)
            if d.get("rel_type") == "CALLS"
        )
        if start not in call_graph:
            return [start] if start in self._g else []
        return list(nx.bfs_tree(call_graph, start).nodes())

    def has_cycle(self) -> bool:
        """True if the graph contains any directed cycle."""
        try:
            nx.find_cycle(self._g)
            return True
        except nx.NetworkXNoCycle:
            return False

    def find_cycles(self) -> list[list[str]]:
        """Return all simple cycles."""
        return list(nx.simple_cycles(self._g))

    def node_count(self) -> int:
        return self._g.number_of_nodes()

    def edge_count(self) -> int:
        return self._g.number_of_edges()

    def get_node_attrs(self, node_id: str) -> dict:
        return dict(self._g.nodes.get(node_id, {}))

    def successors(self, node_id: str) -> list[str]:
        return list(self._g.successors(node_id))

    def predecessors(self, node_id: str) -> list[str]:
        return list(self._g.predecessors(node_id))
