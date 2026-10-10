"""Evidence gathering for the agent's ACT step.

Every Evidence item produced here carries a real "file:line" source:
  - retrieval : hybrid BM25 + vector hits from the indexed code chunks
  - ripgrep   : literal keyword matches in the repository files
  - graph     : CALLS edges from the knowledge graph for the top hits
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Optional

from archon.agent.harness import ToolCallLimitError, ToolNotPermittedError
from archon.agent.loop import Evidence

log = logging.getLogger(__name__)

def _bounded_env_int(name: str, default: int, low: int, high: int) -> int:
    try:
        return max(low, min(high, int(os.getenv(name, str(default)))))
    except (TypeError, ValueError):
        return default


MAX_EVIDENCE = _bounded_env_int("ARCHON_MAX_EVIDENCE", 24, 4, 100)

_STOP = {
    "locate", "review", "files", "file", "code", "and", "the", "for", "with", "from",
    "that", "this", "into", "any", "all", "how", "what", "trace", "flow", "map",
    "identify", "document", "analyze", "analyse", "overall", "key", "including",
    "understand", "investigate", "explain", "find", "list", "show", "main", "most",
    "through", "between", "their", "them", "your", "over", "about", "using", "used",
    "where", "which", "when", "does", "work", "works", "system", "points", "point",
    "custom", "static", "dynamic", "mechanisms", "mechanism", "decision", "incoming",
}

_SKIP_PREFIXES = ("tests/", "test/", "docs/", "doc/", "examples/")


def extract_keywords(text: str, n: int = 3) -> list[str]:
    """Pick up to n distinctive identifier-like words from free text."""
    out: list[str] = []
    for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", text.lower()):
        if w not in _STOP and w not in out:
            out.append(w)
    return out[:n]


def is_source_path(path: str) -> bool:
    """True for library code; False for tests, docs and examples."""
    p = path.replace("\\", "/")
    base = p.rsplit("/", 1)[-1]
    return not (p.startswith(_SKIP_PREFIXES) or "/tests/" in p
                or base.startswith("test_") or base == "conftest.py")


_IMPORT_OR_COMMENT = re.compile(r"^\s*(from\s+\S+\s+import\b|import\s+\S+|#)")
_DEF_LINE = re.compile(r"^\s*(async\s+def|def|class)\s+")


def _match_score(text: str, kw: str) -> int:
    """Higher = more informative hit. Definitions beat usages; keyword in the
    definition's name beats keyword in its body/arguments."""
    score = 0
    if _DEF_LINE.match(text):
        score += 3
        head = text.split("(")[0].lower()
        if kw in head:
            score += 2
    elif text.lstrip().startswith("@"):
        score += 2
    return score


def _rel(path: str, repo_root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(repo_root.resolve()).as_posix()
    except (ValueError, OSError):
        return path.replace("\\", "/")


def gather_evidence(
    task: str,
    ctx_engine,
    repo_root: str | Path,
    harness=None,
    store=None,
    retries: int = 0,
    extra_terms: Optional[list[str]] = None,
) -> list[Evidence]:
    """Collect evidence for one investigation task. Retries widen the search."""
    root = Path(repo_root)
    evidence: list[Evidence] = []
    seen: set[tuple[str, str]] = set()

    def add(source: str, content: str, tool: str) -> None:
        key = (source, content[:80])
        if key in seen or len(evidence) >= MAX_EVIDENCE:
            return
        seen.add(key)
        evidence.append(Evidence(source=source, content=content.strip()[:300], tool=tool))

    # 1) hybrid retrieval over indexed functions/classes -----------------------
    base_top_k = _bounded_env_int("ARCHON_RETRIEVAL_TOP_K", 8, 1, 40)
    top_k = base_top_k + (base_top_k // 2) * retries
    # over-fetch, then drop tests/docs: otherwise test files can fill the whole top-k
    query = task + (" " + " ".join(extra_terms) if extra_terms else "")
    chunks = ctx_engine.query(query, top_k=top_k * 4)
    src_chunks = [c for c in chunks if is_source_path(c.file_path)] or chunks
    for c in src_chunks[:top_k]:
        add(f"{c.file_path}:{c.line_start}", c.text, "retrieval")

    # 2) ripgrep keyword hits (imports/comments dropped, definitions ranked first)
    from archon.tools.search import ripgrep
    kws = list(dict.fromkeys([t.lower() for t in (extra_terms or [])][:5]
                             + extract_keywords(task, n=3 + retries)))
    for kw in kws:
        try:
            if harness is not None:
                tc = harness.call("ripgrep", ripgrep, pattern=kw, path=str(root),
                                  max_results=5000, ignore_case=True)
                matches = tc.output or []
            else:
                matches = ripgrep(kw, root, max_results=5000, ignore_case=True)
        except (ToolNotPermittedError, ToolCallLimitError) as e:
            log.info("ripgrep skipped: %s", e)
            break
        scored = []
        for m in matches:
            rel = _rel(m.file, root)
            if not rel.endswith(".py") or not is_source_path(rel):
                continue
            if _IMPORT_OR_COMMENT.match(m.text):
                continue
            scored.append((-_match_score(m.text, kw), rel, m.line, m.text))
        scored.sort()
        for _, rel, line, text in scored[:4]:
            add(f"{rel}:{line}", text, "ripgrep")

    # 3) call-graph neighbours of the top retrieval hits ------------------------
    if store is not None:
        for c in src_chunks[:3]:
            node = store.get_node(c.id)
            if node is None:
                continue
            for e in [e for e in store.edges_from(c.id) if e.rel_type == "CALLS"][:3]:
                add(node.provenance or f"{c.file_path}:{c.line_start}",
                    f"{c.id} calls {e.target_id}", "graph")

    return evidence
