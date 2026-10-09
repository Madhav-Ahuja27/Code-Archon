"""Build the knowledge graph (nodes + edges) from a ParseResult.

Edge resolution is name-based (static, no type inference), so CALLS and
INHERITS edges are heuristic and tagged resolution="heuristic". Ambiguous
names are skipped rather than guessed, to avoid false edges.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath

from archon.graph.neo4j_client import GraphEdge, GraphNode

# Method names shared with builtins / stdlib containers. A call like `x.get()`
# says nothing about a user-defined `get`, so never link these across modules.
_NOISE_NAMES = {
    "get", "set", "append", "items", "keys", "values", "update", "pop", "add",
    "join", "split", "format", "read", "write", "open", "close", "copy",
    "extend", "remove", "sort", "strip", "lower", "upper", "encode", "decode",
    "startswith", "endswith", "replace", "find", "index", "count", "insert",
    "clear", "setdefault", "run", "call", "send", "print", "len", "str", "int",
    "list", "dict", "tuple", "isinstance", "getattr", "setattr", "hasattr",
    "super", "type", "iter", "next", "range", "sorted", "min", "max", "sum",
}


def _dotted(module_id: str) -> str:
    """'pkg/sub/mod.py' -> 'pkg.sub.mod'; 'pkg/__init__.py' -> 'pkg'."""
    p = PurePosixPath(module_id)
    parts = list(p.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _build_module_index(module_ids: list[str]) -> dict[str, list[str]]:
    """Map every dotted suffix of each module path to the module ids it could mean."""
    idx: dict[str, list[str]] = defaultdict(list)
    for mid in module_ids:
        parts = _dotted(mid).split(".")
        for i in range(len(parts)):
            idx[".".join(parts[i:])].append(mid)
    return idx


def _resolve_import(name: str, idx: dict[str, list[str]], self_id: str) -> str | None:
    """Resolve an imported dotted name to a repo module. Longest prefix wins;
    only unique matches are accepted."""
    parts = name.split(".")
    for end in range(len(parts), 0, -1):
        cands = [m for m in idx.get(".".join(parts[:end]), []) if m != self_id]
        if len(cands) == 1:
            return cands[0]
        if len(cands) > 1:
            return None     # ambiguous -> skip
    return None


def build_graph(parse_result, store) -> dict[str, int]:
    """Populate `store` with nodes and edges. Returns counts per kind."""
    counts = defaultdict(int)

    # ── Nodes ────────────────────────────────────────────────────────────────
    for mod in parse_result.modules:
        store.upsert_node(GraphNode(
            id=mod.id, label="Module",
            properties={"path": mod.path, "line_count": mod.line_count,
                        "avg_complexity": mod.avg_complexity},
            confidence=0.9, provenance=f"{mod.id}:1",
        ))
        counts["modules"] += 1
    for cls in parse_result.classes:
        store.upsert_node(GraphNode(
            id=cls.id, label="Class",
            properties={"name": cls.name, "module_path": cls.module_path},
            confidence=0.9, provenance=f"{cls.module_path}:{cls.line_start}",
        ))
        counts["classes"] += 1
    for fn in parse_result.functions:
        store.upsert_node(GraphNode(
            id=fn.id, label="Function",
            properties={"name": fn.name, "module_path": fn.module_path,
                        "complexity": fn.complexity},
            confidence=0.9, provenance=f"{fn.module_path}:{fn.line_start}",
        ))
        counts["functions"] += 1

    def edge(src: str, tgt: str, rel: str, heuristic: bool = False) -> None:
        store.upsert_edge(GraphEdge(
            source_id=src, target_id=tgt, rel_type=rel,
            properties={"resolution": "heuristic"} if heuristic else {},
        ))
        counts[rel.lower()] += 1

    # ── CONTAINS ─────────────────────────────────────────────────────────────
    for cls in parse_result.classes:
        edge(cls.module_path, cls.id, "CONTAINS")
    for fn in parse_result.functions:
        edge(fn.module_path, fn.id, "CONTAINS")

    # ── IMPORTS ──────────────────────────────────────────────────────────────
    mod_idx = _build_module_index([m.id for m in parse_result.modules])
    for mod in parse_result.modules:
        targets = {_resolve_import(i, mod_idx, mod.id) for i in mod.imports}
        for tgt in sorted(t for t in targets if t):
            edge(mod.id, tgt, "IMPORTS")

    # ── INHERITS ─────────────────────────────────────────────────────────────
    classes_by_name: dict[str, list] = defaultdict(list)
    for cls in parse_result.classes:
        classes_by_name[cls.name].append(cls)
    for cls in parse_result.classes:
        for base in cls.bases:
            simple = base.split(".")[-1]
            cands = classes_by_name.get(simple, [])
            same_mod = [c for c in cands if c.module_path == cls.module_path and c.id != cls.id]
            pick = same_mod if same_mod else [c for c in cands if c.id != cls.id]
            if len(pick) == 1:
                edge(cls.id, pick[0].id, "INHERITS", heuristic=True)

    # ── CALLS ────────────────────────────────────────────────────────────────
    fns_by_name: dict[str, list] = defaultdict(list)
    for fn in parse_result.functions:
        fns_by_name[fn.name].append(fn)
    for fn in parse_result.functions:
        for called in fn.calls:
            cands = [c for c in fns_by_name.get(called, []) if c.id != fn.id]
            if not cands:
                continue
            same_mod = [c for c in cands if c.module_path == fn.module_path]
            if len(same_mod) > 1 and fn.class_name:
                same_cls = [c for c in same_mod if c.class_name == fn.class_name]
                same_mod = same_cls or same_mod
            if len(same_mod) == 1:
                edge(fn.id, same_mod[0].id, "CALLS", heuristic=True)
            elif not same_mod and len(cands) == 1 and called not in _NOISE_NAMES:
                edge(fn.id, cands[0].id, "CALLS", heuristic=True)

    return dict(counts)
