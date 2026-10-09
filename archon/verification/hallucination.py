"""Hallucination filter — blocks ungrounded claims from graph promotion."""

from __future__ import annotations

import re
import logging
from enum import Enum
from typing import Optional

from pydantic import BaseModel

log = logging.getLogger(__name__)

# Pattern: "file.py:42" or "path/to/file.py:100"
_PROVENANCE_RE = re.compile(
    r'\b[\w/\\.-]+\.(?:py|pyi|rst|md|txt|cfg|toml|ini|ya?ml|json|html|js|c|h):\d+\b'
)


class FilterStatus(str, Enum):
    PASSES = "PASSES"
    HALLUCINATED = "HALLUCINATED"


class FilterResult(BaseModel):
    status: FilterStatus
    claim: str
    provenance_found: list[str] = []
    reason: str = ""


def check_claim(
    claim: str,
    evidence_texts: list[str],
) -> FilterResult:
    """Check whether a claim is traceable to at least one evidence item.

    A claim passes if at least one evidence text contains a file:line
    provenance reference (e.g. "auth.py:42").

    Args:
        claim: The hypothesis text to check.
        evidence_texts: Raw text content from tool outputs / evidence items.

    Returns:
        FilterResult with PASSES or HALLUCINATED status.
    """
    all_provenances: list[str] = []
    for text in evidence_texts:
        found = _PROVENANCE_RE.findall(text)
        all_provenances.extend(found)

    if all_provenances:
        return FilterResult(
            status=FilterStatus.PASSES,
            claim=claim,
            provenance_found=all_provenances,
            reason=f"Traceable to {len(all_provenances)} source location(s)",
        )

    return FilterResult(
        status=FilterStatus.HALLUCINATED,
        claim=claim,
        provenance_found=[],
        reason="No file:line provenance found in evidence",
    )


def promote_to_graph(
    claim: str,
    evidence_texts: list[str],
    store,
    confidence: float = 0.8,
    node_id: Optional[str] = None,
) -> Optional[FilterResult]:
    """Attempt to write a verified claim to the graph store.

    Blocks write and returns HALLUCINATED if no provenance found.
    Returns FilterResult on success or hallucination.
    """
    from archon.graph.neo4j_client import GraphNode

    result = check_claim(claim, evidence_texts)

    if result.status == FilterStatus.HALLUCINATED:
        log.warning("Hallucination blocked: %s", claim[:80])
        return result

    # Write to graph
    nid = node_id or f"verified::{hash(claim) & 0xFFFFFF}"
    provenance = result.provenance_found[0] if result.provenance_found else ""
    store.upsert_node(GraphNode(
        id=nid,
        label="Hypothesis",
        properties={"claim": claim},
        confidence=confidence,
        provenance=provenance,
    ))
    log.info("Promoted verified claim: %s (conf=%.2f)", claim[:60], confidence)
    return result


def _file_of(ref: str) -> str:
    return ref.rsplit(":", 1)[0].replace("\\", "/")


def _line_of(ref: str) -> int:
    try:
        return int(ref.rsplit(":", 1)[1])
    except (IndexError, ValueError):
        return -1


def _same_file(a: str, b: str) -> bool:
    a, b = a.replace("\\", "/"), b.replace("\\", "/")
    return a == b or a.endswith("/" + b) or b.endswith("/" + a)


def check_claim_grounded(
    claim: str,
    evidence: list[tuple[str, str]],
    require_citation: bool = False,
) -> FilterResult:
    """Strict gate used by the agent loop.

    `evidence` is a list of (source, content) pairs, source being "file:line".
    - Evidence without any file:line source cannot ground anything.
    - If the claim cites file:line references, every cited file AND line must be
      one the evidence actually showed (fabricated file or line => HALLUCINATED).
    - If the claim cites nothing: rejected when require_citation, otherwise the
      evidence sources themselves serve as provenance (heuristic mode).
    """
    ev_refs = [src for src, _ in evidence if _PROVENANCE_RE.search(src or "")]
    if not ev_refs:
        return FilterResult(status=FilterStatus.HALLUCINATED, claim=claim,
                            reason="No evidence item carries file:line provenance")
    cited = _PROVENANCE_RE.findall(claim)
    if cited:
        bad = [
            c for c in cited
            if not any(_same_file(_file_of(c), _file_of(r)) and _line_of(c) == _line_of(r)
                       for r in ev_refs)
        ]
        if bad:
            return FilterResult(status=FilterStatus.HALLUCINATED, claim=claim,
                                reason=f"Claim cites file:line not shown in evidence: {bad}")
        return FilterResult(status=FilterStatus.PASSES, claim=claim,
                            provenance_found=cited,
                            reason=f"{len(cited)} citation(s) match evidence exactly")
    if require_citation:
        return FilterResult(status=FilterStatus.HALLUCINATED, claim=claim,
                            reason="Claim cites no file:line source")
    return FilterResult(status=FilterStatus.PASSES, claim=claim,
                        provenance_found=ev_refs[:3],
                        reason="Grounded in evidence sources (uncited claim)")
