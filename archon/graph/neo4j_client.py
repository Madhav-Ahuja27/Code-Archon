"""Neo4j graph client.

Stores and queries ModuleNode, ClassNode, FunctionNode as a property graph.
Falls back to in-memory mock when Neo4j is unavailable (for testing without Docker).
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from pydantic import BaseModel

log = logging.getLogger(__name__)


# ── Graph node / edge models ──────────────────────────────────────────────────

class GraphNode(BaseModel):
    id: str
    label: str                      # Module | Class | Function | Hypothesis | Evidence
    properties: dict[str, Any]
    confidence: float = 0.5
    provenance: str = ""            # "file.py:42"


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    rel_type: str                   # IMPORTS | CALLS | INHERITS | CONTAINS | SUPPORTS
    properties: dict[str, Any] = {}


# ── In-memory store (used when Neo4j unavailable) ────────────────────────────

class _InMemoryStore:
    """Minimal in-memory graph store used in tests / offline mode."""

    def __init__(self):
        self._nodes: dict[str, GraphNode] = {}
        self._edges: list[GraphEdge] = []

    def upsert_node(self, node: GraphNode) -> None:
        self._nodes[node.id] = node

    def upsert_edge(self, edge: GraphEdge) -> None:
        # deduplicate by (source, target, rel_type)
        key = (edge.source_id, edge.target_id, edge.rel_type)
        self._edges = [
            e for e in self._edges
            if (e.source_id, e.target_id, e.rel_type) != key
        ]
        self._edges.append(edge)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def all_nodes(self) -> list[GraphNode]:
        return list(self._nodes.values())

    def all_edges(self) -> list[GraphEdge]:
        return list(self._edges)

    def nodes_by_label(self, label: str) -> list[GraphNode]:
        return [n for n in self._nodes.values() if n.label == label]

    def edges_by_type(self, rel_type: str) -> list[GraphEdge]:
        return [e for e in self._edges if e.rel_type == rel_type]

    def edges_from(self, node_id: str) -> list[GraphEdge]:
        return [e for e in self._edges if e.source_id == node_id]

    def edges_to(self, node_id: str) -> list[GraphEdge]:
        return [e for e in self._edges if e.target_id == node_id]

    def low_confidence_nodes(self, threshold: float) -> list[GraphNode]:
        return [n for n in self._nodes.values() if n.confidence < threshold]

    def clear(self) -> None:
        self._nodes.clear()
        self._edges.clear()

    def node_count(self) -> int:
        return len(self._nodes)


# ── Neo4j-backed store ────────────────────────────────────────────────────────

class _Neo4jStore:
    """Production graph store backed by Neo4j bolt."""

    def __init__(self, uri: str, user: str, password: str):
        from neo4j import GraphDatabase
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def upsert_node(self, node: GraphNode) -> None:
        cypher = (
            f"MERGE (n:{node.label} {{id: $id}}) "
            "SET n += $props, n.confidence = $confidence, n.provenance = $provenance"
        )
        with self._driver.session() as s:
            s.run(cypher, id=node.id, props=node.properties,
                  confidence=node.confidence, provenance=node.provenance)

    def upsert_edge(self, edge: GraphEdge) -> None:
        cypher = (
            "MATCH (a {id: $src}), (b {id: $tgt}) "
            f"MERGE (a)-[r:{edge.rel_type}]->(b) "
            "SET r += $props"
        )
        with self._driver.session() as s:
            s.run(cypher, src=edge.source_id, tgt=edge.target_id, props=edge.properties)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        with self._driver.session() as s:
            result = s.run("MATCH (n {id: $id}) RETURN n LIMIT 1", id=node_id)
            record = result.single()
            if not record:
                return None
            n = record["n"]
            labels = list(n.labels)
            label = labels[0] if labels else "Unknown"
            props = dict(n)
            confidence = props.pop("confidence", 0.5)
            provenance = props.pop("provenance", "")
            props.pop("id", None)
            return GraphNode(id=node_id, label=label, properties=props,
                             confidence=confidence, provenance=provenance)

    def nodes_by_label(self, label: str) -> list[GraphNode]:
        with self._driver.session() as s:
            result = s.run(f"MATCH (n:{label}) RETURN n")
            nodes = []
            for record in result:
                n = record["n"]
                props = dict(n)
                nid = props.pop("id", "")
                confidence = props.pop("confidence", 0.5)
                provenance = props.pop("provenance", "")
                nodes.append(GraphNode(id=nid, label=label, properties=props,
                                       confidence=confidence, provenance=provenance))
            return nodes

    def low_confidence_nodes(self, threshold: float) -> list[GraphNode]:
        with self._driver.session() as s:
            result = s.run(
                "MATCH (n) WHERE n.confidence < $t RETURN n", t=threshold
            )
            out = []
            for record in result:
                n = record["n"]
                props = dict(n)
                nid = props.pop("id", "")
                confidence = props.pop("confidence", 0.5)
                provenance = props.pop("provenance", "")
                labels = list(n.labels)
                label = labels[0] if labels else "Unknown"
                out.append(GraphNode(id=nid, label=label, properties=props,
                                     confidence=confidence, provenance=provenance))
            return out

    def clear(self) -> None:
        with self._driver.session() as s:
            s.run("MATCH (n) DETACH DELETE n")

    def node_count(self) -> int:
        with self._driver.session() as s:
            result = s.run("MATCH (n) RETURN count(n) AS c")
            return result.single()["c"]

    def all_nodes(self) -> list[GraphNode]:
        out: list[GraphNode] = []
        for label in ("Module", "Class", "Function", "Hypothesis", "Evidence", "Dependency"):
            out += self.nodes_by_label(label)
        return out

    def all_edges(self) -> list[GraphEdge]:
        with self._driver.session() as s:
            result = s.run(
                "MATCH (a)-[r]->(b) RETURN a.id AS src, b.id AS tgt, type(r) AS rel"
            )
            return [
                GraphEdge(source_id=rec["src"], target_id=rec["tgt"],
                          rel_type=rec["rel"])
                for rec in result
            ]

    def edges_from(self, node_id: str) -> list[GraphEdge]:
        with self._driver.session() as s:
            result = s.run(
                "MATCH (a {id: $id})-[r]->(b) RETURN b.id AS tgt, type(r) AS rel",
                id=node_id
            )
            return [GraphEdge(source_id=node_id, target_id=r["tgt"],
                              rel_type=r["rel"]) for r in result]

    def edges_to(self, node_id: str) -> list[GraphEdge]:
        with self._driver.session() as s:
            result = s.run(
                "MATCH (a)-[r]->(b {id: $id}) RETURN a.id AS src, type(r) AS rel",
                id=node_id
            )
            return [GraphEdge(source_id=r["src"], target_id=node_id,
                              rel_type=r["rel"]) for r in result]

    def edges_by_type(self, rel_type: str) -> list[GraphEdge]:
        with self._driver.session() as s:
            result = s.run(
                f"MATCH (a)-[r:{rel_type}]->(b) RETURN a.id AS src, b.id AS tgt"
            )
            return [GraphEdge(source_id=r["src"], target_id=r["tgt"],
                              rel_type=rel_type) for r in result]


# ── Public factory ────────────────────────────────────────────────────────────

def _port_open(uri: str, timeout: float = 1.0) -> bool:
    """True if something is listening on the Neo4j bolt port."""
    import socket
    from urllib.parse import urlparse
    u = urlparse(uri)
    try:
        socket.create_connection((u.hostname or "localhost", u.port or 7687), timeout).close()
        return True
    except OSError:
        return False


def make_graph_store(
    uri: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    force_inmemory: bool = False,
    wait: float = 0.0,
) -> _InMemoryStore | _Neo4jStore:
    """Return a Neo4j store if reachable, else fall back to in-memory.

    `wait` (seconds): if the bolt port is open but Neo4j is not ready yet
    (it takes ~20-30 s to boot), keep retrying instead of falling back.
    If nothing is listening at all, fall back immediately.
    """
    import time
    if force_inmemory:
        return _InMemoryStore()
    from archon.config import cfg
    u = uri or cfg.neo4j_uri
    usr = user or cfg.neo4j_user
    pw = password or cfg.neo4j_password
    deadline = time.monotonic() + wait
    while True:
        try:
            store = _Neo4jStore(u, usr, pw)
            store._driver.verify_connectivity()
            log.info("Connected to Neo4j at %s", u)
            return store
        except Exception as e:
            if wait and time.monotonic() < deadline and _port_open(u):
                log.info("Neo4j is starting up, waiting...")
                time.sleep(2)
                continue
            log.warning("Neo4j unavailable (%s) — using in-memory store", e)
            return _InMemoryStore()
