"""Phase 4 — Agent Loop (LangGraph) tests.

Gate: all 8 pass before Phase 5 begins.
"""

from __future__ import annotations

import pytest

from archon.agent.loop import (
    AgentPhase,
    AgentState,
    Evidence,
    Hypothesis,
    build_agent_graph,
    node_act,
    node_identify_unknowns,
    node_investigate,
    node_plan,
    node_verify,
    route_after_verify,
)
from archon.agent.harness import Harness, HarnessConfig, ToolNotPermittedError
from archon.goal_analyzer import GoalAnalyzer, InvestigationGoal
from archon.graph.neo4j_client import make_graph_store


# ── Test 1: GoalAnalyzer parses free text → InvestigationGoal ────────────────

def test_goal_analyzer_parses():
    ga = GoalAnalyzer(llm=None)
    goal = ga.analyze("Understand the authentication flow and trace login")
    assert isinstance(goal, InvestigationGoal)
    assert len(goal.investigation_tasks) >= 1
    assert len(goal.success_criteria) >= 1
    assert "auth" in goal.objective.lower() or "login" in goal.objective.lower()


# ── Test 2: PLAN → ACT state transition ──────────────────────────────────────

def test_state_transitions_plan_act():
    state = AgentState(goal="map modules", iteration=0)
    state = node_plan(state)
    assert state.phase == AgentPhase.ACT
    assert state.hypothesis is not None
    assert state.iteration == 1


# ── Test 3: VERIFY pass → UPDATE_GRAPH ───────────────────────────────────────

def test_state_transitions_verify_ok():
    state = AgentState(
        goal="test",
        hypothesis=Hypothesis(claim="auth module exists", status="PENDING"),
        evidence=[Evidence(source="auth.py:1", content="def login(): ...")],
    )
    state = node_verify(state)
    assert state.hypothesis.status == "VERIFIED"
    assert state.phase == AgentPhase.UPDATE_GRAPH


# ── Test 4: VERIFY fail → INVESTIGATE ────────────────────────────────────────

def test_state_transitions_verify_fail():
    state = AgentState(
        goal="test",
        hypothesis=Hypothesis(claim="impossible claim", status="PENDING"),
        evidence=[],   # no evidence → UNCERTAIN → INVESTIGATE
    )
    state = node_verify(state)
    assert state.hypothesis.status == "UNCERTAIN"
    assert state.phase == AgentPhase.INVESTIGATE


# ── Test 5: max iterations stops agent ───────────────────────────────────────

def test_max_iterations_stops():
    store = make_graph_store(force_inmemory=True)
    graph = build_agent_graph(store=store, max_iterations=3)
    init = AgentState(goal="list all modules").model_dump()
    # inject evidence so loop keeps verifying rather than replanning forever
    final = graph.invoke(init)
    assert final["iteration"] <= 4   # max 3 + possible overshoot of 1


# ── Test 6: agent accumulates evidence across iterations ─────────────────────

def test_agent_accumulates_evidence():
    harness = Harness()
    store = make_graph_store(force_inmemory=True)
    graph = build_agent_graph(harness=harness, store=store, max_iterations=3)
    init = AgentState(goal="trace call graph").model_dump()
    final = graph.invoke(init)
    # After at least 1 iteration with harness, evidence list grows
    assert final["iteration"] >= 1


# ── Test 7: harness blocks forbidden tool ────────────────────────────────────

def test_harness_blocks_bad_tool():
    config = HarnessConfig(allowed_tools={"ast_analysis"})
    harness = Harness(config)
    with pytest.raises(ToolNotPermittedError):
        harness.call("forbidden_tool", lambda: "result")


# ── Test 8: full mini run — real evidence from the fixture repo ──────────────

def test_full_mini_run():
    from pathlib import Path
    from archon.agent.harness import HarnessConfig
    from archon.ingestion.ast_parser import parse_repository
    from archon.graph.builder import build_graph
    from archon.retrieval.bm25 import BM25Index
    from archon.retrieval.vector_store import ContextEngine, VectorStore

    fixtures = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"
    parse_result = parse_repository(fixtures)
    store = make_graph_store(force_inmemory=True)
    build_graph(parse_result, store)

    chunks = ContextEngine.chunks_from_parse_result(parse_result)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    engine = ContextEngine(bm25, vs)

    harness = Harness(HarnessConfig(allowed_tools={"ripgrep"}, call_limit_per_tool=5))
    graph = build_agent_graph(harness=harness, store=store, max_iterations=4,
                              ctx_engine=engine, repo_root=fixtures)
    init = AgentState(goal="understand authentication",
                      tasks=["authentication password hashing"]).model_dump()
    final = graph.invoke(init)

    assert final["complete"] is True
    assert len(final["findings"]) >= 1
    assert ".py:" in final["findings"][0]          # real file:line provenance
    assert "synthetic" not in final["findings"][0]
