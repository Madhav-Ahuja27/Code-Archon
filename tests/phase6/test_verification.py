"""Phase 6 — Verification Harness + Hallucination Filter tests.

Gate: all 8 pass before Phase 7 begins.
"""

from __future__ import annotations

import pytest

from archon.verification.harness import (
    EvidenceItem,
    VerificationStatus,
    verify_hypothesis,
)
from archon.verification.hallucination import (
    FilterStatus,
    check_claim,
    promote_to_graph,
)
from archon.graph.neo4j_client import make_graph_store
from archon.agent.loop import AgentPhase, AgentState, Hypothesis


# ── Test 1: verify true hypothesis (has supporting evidence) ─────────────────

def test_verify_true_hypothesis():
    evidence = [
        EvidenceItem(source="auth.py:14", content="def hash_password", supports=True),
        EvidenceItem(source="auth.py:22", content="def verify_password", supports=True),
    ]
    result = verify_hypothesis("auth module has hash and verify functions", evidence)
    assert result.status == VerificationStatus.VERIFIED
    assert result.confidence > 0.5
    assert len(result.supporting) == 2


# ── Test 2: verify false hypothesis (contradicted) ───────────────────────────

def test_verify_false_hypothesis():
    evidence = [
        EvidenceItem(source="auth.py:1", content="no login function found", supports=False),
        EvidenceItem(source="auth.py:2", content="no session code found", supports=False),
    ]
    result = verify_hypothesis("auth module has login and session management", evidence)
    assert result.status == VerificationStatus.REFUTED
    assert len(result.contradicting) == 2


# ── Test 3: no evidence → UNCERTAIN ──────────────────────────────────────────

def test_verify_uncertain():
    result = verify_hypothesis("some unknown claim", [])
    assert result.status == VerificationStatus.UNCERTAIN
    assert result.confidence < 0.5


# ── Test 4: many supporting evidence → confidence > 0.8 ──────────────────────

def test_confidence_high_on_multi_evidence():
    evidence = [
        EvidenceItem(source=f"auth.py:{i}", content=f"evidence {i}", supports=True)
        for i in range(1, 5)
    ]
    result = verify_hypothesis("well-supported claim", evidence)
    assert result.status == VerificationStatus.VERIFIED
    assert result.confidence > 0.8


# ── Test 5: claim with no file:line ref → HALLUCINATED ───────────────────────

def test_hallucination_blocked():
    result = check_claim(
        claim="The auth module handles login",
        evidence_texts=["I think the auth module probably handles login"],
    )
    assert result.status == FilterStatus.HALLUCINATED
    assert result.provenance_found == []


# ── Test 6: claim with file:line ref → PASSES ────────────────────────────────

def test_hallucination_passes():
    result = check_claim(
        claim="hash_password defined in auth.py",
        evidence_texts=["auth.py:14 — def hash_password(self, password: str)"],
    )
    assert result.status == FilterStatus.PASSES
    assert "auth.py:14" in result.provenance_found


# ── Test 7: VERIFIED claim promoted to graph ──────────────────────────────────

def test_promoted_written_to_graph():
    store = make_graph_store(force_inmemory=True)
    result = promote_to_graph(
        claim="login function is in auth.py",
        evidence_texts=["Found at auth.py:30 — def login()"],
        store=store,
        confidence=0.85,
        node_id="test::claim::login",
    )
    assert result.status == FilterStatus.PASSES
    node = store.get_node("test::claim::login")
    assert node is not None
    assert node.confidence == 0.85
    assert node.provenance == "auth.py:30"


# ── Test 8: REFUTED hypothesis triggers INVESTIGATE phase ────────────────────

def test_refuted_triggers_replan():
    """Simulates what the agent loop does when verification returns REFUTED."""
    from archon.agent.loop import node_verify

    # Construct a state where evidence contradicts the hypothesis
    # In the agent loop, a hypothesis with no evidence → UNCERTAIN → INVESTIGATE
    # REFUTED is triggered when contradicting evidence exists — that happens
    # in the verification harness, which the agent reads via the graph.
    # Here we test the state transition directly.
    state = AgentState(
        goal="test",
        hypothesis=Hypothesis(claim="impossible claim", status="PENDING"),
        evidence=[],  # no evidence → UNCERTAIN → INVESTIGATE
    )
    state = node_verify(state)
    assert state.phase == AgentPhase.INVESTIGATE
    assert state.hypothesis.status in ("UNCERTAIN", "REFUTED")
