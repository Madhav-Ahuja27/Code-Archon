"""Verification Harness — validates hypotheses against evidence."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    REFUTED = "REFUTED"
    UNCERTAIN = "UNCERTAIN"


class EvidenceItem(BaseModel):
    source: str        # "file.py:42"
    content: str
    supports: bool     # True = supports hypothesis, False = contradicts


class VerificationResult(BaseModel):
    status: VerificationStatus
    confidence: float
    supporting: list[EvidenceItem] = Field(default_factory=list)
    contradicting: list[EvidenceItem] = Field(default_factory=list)
    reason: str = ""


def verify_hypothesis(
    claim: str,
    evidence_list: list[EvidenceItem],
) -> VerificationResult:
    """Verify a claim against a list of evidence items.

    Rules:
    - 0 evidence → UNCERTAIN, confidence 0.3
    - contradicting > supporting → REFUTED
    - supporting ≥ 1 and supporting > contradicting → VERIFIED
    - supporting > 0 but low margin → UNCERTAIN, mid confidence
    """
    supporting = [e for e in evidence_list if e.supports]
    contradicting = [e for e in evidence_list if not e.supports]

    if not evidence_list:
        return VerificationResult(
            status=VerificationStatus.UNCERTAIN,
            confidence=0.3,
            reason="No evidence provided",
        )

    if contradicting and len(contradicting) >= len(supporting):
        return VerificationResult(
            status=VerificationStatus.REFUTED,
            confidence=0.8,
            supporting=supporting,
            contradicting=contradicting,
            reason=f"Refuted by {len(contradicting)} contradicting evidence items",
        )

    if supporting:
        # confidence scales with evidence count, capped at 0.95
        confidence = min(0.5 + 0.15 * len(supporting), 0.95)
        return VerificationResult(
            status=VerificationStatus.VERIFIED,
            confidence=confidence,
            supporting=supporting,
            contradicting=contradicting,
            reason=f"Supported by {len(supporting)} evidence items",
        )

    return VerificationResult(
        status=VerificationStatus.UNCERTAIN,
        confidence=0.4,
        reason="Insufficient evidence",
    )
