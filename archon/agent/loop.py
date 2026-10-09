"""LangGraph agent loop — Plan → Act → Observe → Verify, one task at a time.

  PLAN ─► ACT ─► OBSERVE ─► VERIFY ─┬─ verified ─► UPDATE_GRAPH ─┬─ accepted ─► IDENTIFY_UNKNOWNS ─► PLAN | COMPLETE
   ▲                                │                            └─ rejected by provenance gate ─┐
   └──────────── INVESTIGATE ◄──────┴─ refuted / uncertain ◄───────────────────────────────────────┘

* ACT gathers real evidence (retrieval + ripgrep + graph) when a context engine
  and repo root are supplied. Without them it falls back to a mechanics-only
  placeholder that can never pass the provenance gate.
* UPDATE_GRAPH is the hallucination gate: a claim is written to the graph only
  if its evidence carries file:line provenance (and, in LLM mode, every file it
  cites appears in that evidence).
* Each task gets MAX_RETRIES_PER_TASK retries; tasks that never verify are
  reported in `unknowns` instead of looping forever.
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Any, Optional

from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

MAX_RETRIES_PER_TASK = 2
_PROMPT_EVIDENCE_ITEMS = 14


# ── State ─────────────────────────────────────────────────────────────────────

class AgentPhase(str, Enum):
    PLAN = "PLAN"
    ACT = "ACT"
    OBSERVE = "OBSERVE"
    VERIFY = "VERIFY"
    UPDATE_GRAPH = "UPDATE_GRAPH"
    IDENTIFY_UNKNOWNS = "IDENTIFY_UNKNOWNS"
    INVESTIGATE = "INVESTIGATE"
    COMPLETE = "COMPLETE"


class Evidence(BaseModel):
    source: str          # "file.py:42"
    content: str
    tool: str = ""


class Hypothesis(BaseModel):
    claim: str
    confidence: float = 0.5
    status: str = "PENDING"   # PENDING | VERIFIED | REFUTED | UNCERTAIN | REJECTED


class AgentState(BaseModel):
    goal: str = ""
    current_task: str = ""
    tasks: list[str] = Field(default_factory=list)
    task_index: int = 0
    retries: int = 0
    hypothesis: Optional[Hypothesis] = None
    evidence: list[Evidence] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)    # tasks we could not verify
    rejected: list[str] = Field(default_factory=list)    # claims blocked by the gate
    require_citation: bool = False                       # True when claim came from an LLM
    last_failure: str = ""                               # why the last attempt failed
    search_terms: list[str] = Field(default_factory=list)  # LLM-suggested identifiers (steer search only)
    iteration: int = 0
    phase: AgentPhase = AgentPhase.PLAN
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None
    complete: bool = False


# ── Helpers ───────────────────────────────────────────────────────────────────

def _balanced(evidence: list[Evidence], n: int) -> list[Evidence]:
    """Pick up to n items, round-robin across tools (retrieval / ripgrep / graph) so a
    wide retrieval pool can never crowd keyword and graph evidence out of the prompt."""
    queues: dict[str, list[Evidence]] = {}
    for e in evidence:
        queues.setdefault(e.tool or "", []).append(e)
    out: list[Evidence] = []
    pools = list(queues.values())
    while len(out) < n and any(pools):
        for q in pools:
            if q and len(out) < n:
                out.append(q.pop(0))
    return out


def _format_evidence(evidence: list[Evidence]) -> str:
    return "\n".join(
        f"- [{e.source}] ({e.tool}) {e.content[:200]}"
        for e in _balanced(evidence, _PROMPT_EVIDENCE_ITEMS)
    )


def _llm_text(llm, system: str, human: str) -> Optional[str]:
    from langchain_core.messages import HumanMessage, SystemMessage
    try:
        resp = llm.invoke([SystemMessage(content=system), HumanMessage(content=human)])
        text = resp.content if hasattr(resp, "content") else str(resp)
        return text.strip() or None
    except Exception as e:
        log.warning("LLM call failed (%s)", e)
        return None


def parse_verdict(text: str) -> str:
    """Map free-form LLM output to VERIFIED / REFUTED / UNCERTAIN.
    Word-boundary match so 'UNVERIFIED' or 'not verified' never counts as VERIFIED."""
    t = (text or "").upper()
    if re.search(r"\b(REFUTED|UNVERIFIED|NOT VERIFIED)\b", t):
        return "REFUTED" if "REFUTED" in t else "UNCERTAIN"
    if re.search(r"\bVERIFIED\b", t):
        return "VERIFIED"
    return "UNCERTAIN"


# ── Nodes ─────────────────────────────────────────────────────────────────────

def node_plan(state: AgentState, llm=None, harness=None,
              max_iterations: int = 20) -> AgentState:
    """PLAN: pick the next task and open a fresh hypothesis for it."""
    if not state.tasks:
        state.tasks = [state.current_task or state.goal or "Investigate repository"]

    if state.task_index >= len(state.tasks):
        state.complete = True
        state.phase = AgentPhase.COMPLETE
        return state

    state.iteration += 1
    if state.iteration > max_iterations:
        # budget exhausted: whatever is left is unresolved
        for t in state.tasks[state.task_index:]:
            if t not in state.unknowns:
                state.unknowns.append(t)
        state.complete = True
        state.phase = AgentPhase.COMPLETE
        return state

    state.current_task = state.tasks[state.task_index]
    state.evidence = []
    state.require_citation = False
    state.hypothesis = Hypothesis(claim=state.current_task, confidence=0.5, status="PENDING")
    state.phase = AgentPhase.ACT
    log.info("▶ task %d/%d (attempt %d): %s",
             state.task_index + 1, len(state.tasks), state.retries + 1, state.current_task)
    return state


def node_act(state: AgentState, harness=None, ctx_engine=None,
             repo_root=None, store=None) -> AgentState:
    """ACT: gather evidence. Real tools when ctx_engine+repo_root are given."""
    if harness is not None:
        harness.begin_iteration()
    # Keep an observational trace for the generated report. This does not alter
    # tool selection, evidence, verification, or graph-promotion decisions.
    tool_log_start = len(harness.call_log()) if harness is not None else 0

    if ctx_engine is not None and repo_root is not None:
        from archon.agent.evidence import gather_evidence
        try:
            state.evidence = gather_evidence(
                state.current_task, ctx_engine=ctx_engine, repo_root=repo_root,
                harness=harness, store=store, retries=state.retries,
                extra_terms=state.search_terms,
            )
        except Exception as e:
            state.error = str(e)
            log.warning("evidence gathering failed: %s", e)
    elif harness is not None:
        # Mechanics-only placeholder (no provenance => cannot pass the gate).
        try:
            result = harness.execute_default_tool(state)
            if result:
                state.tool_calls.append(result)
                state.evidence.append(Evidence(
                    source=result.get("source", "tool"),
                    content=str(result.get("output", "")),
                    tool=result.get("tool", ""),
                ))
        except Exception as e:
            state.error = str(e)

    if harness is not None:
        for call in harness.call_log()[tool_log_start:]:
            state.tool_calls.append({
                "tool": call.tool,
                "input": call.input,
                "output": str(call.output)[:500] if call.output is not None else "",
                "error": call.error or "",
                "source": call.source or "",
            })

    state.phase = AgentPhase.OBSERVE
    return state


_SYNTH_SYSTEM = (
    "You are a code archaeologist analysing a legacy Python repository. "
    "Answer the investigation task in 1-3 sentences using ONLY the evidence provided. "
    "Cite every statement with its source exactly as written in the square brackets "
    "of the evidence, e.g. src/pkg/mod.py:123. Never mention files that are not in "
    "the evidence. If the evidence is not enough to answer, reply exactly: INSUFFICIENT"
)


def node_observe(state: AgentState, llm=None) -> AgentState:
    """OBSERVE: with an LLM, turn the raw evidence into a concrete, cited claim."""
    if llm is not None and state.evidence and state.hypothesis is not None:
        text = _llm_text(
            llm, _SYNTH_SYSTEM,
            f"Task: {state.current_task}\n\nEvidence:\n{_format_evidence(state.evidence)}",
        )
        if text:
            state.hypothesis.claim = text
            state.require_citation = True
    state.phase = AgentPhase.VERIFY
    return state


_VERIFY_SYSTEM = (
    "You are a code verification engine. Given a claim and evidence, respond with "
    "ONLY one word: VERIFIED if every statement in the claim is directly supported "
    "by the evidence, REFUTED if the evidence contradicts it, otherwise UNCERTAIN."
)


def _relevant(state: AgentState) -> bool:
    """Heuristic mode: does any evidence mention a keyword of the task/claim?"""
    from archon.agent.evidence import extract_keywords
    text = f"{state.hypothesis.claim} {state.current_task}" if state.hypothesis else state.current_task
    kws = extract_keywords(text, n=6)
    blob = " ".join(f"{e.source} {e.content}" for e in state.evidence).lower()
    return any(k in blob for k in kws)


def node_verify(state: AgentState, llm=None) -> AgentState:
    """VERIFY: is the hypothesis supported by the evidence?"""
    if not state.hypothesis:
        state.phase = AgentPhase.IDENTIFY_UNKNOWNS
        return state

    if state.hypothesis.claim.strip().upper().startswith("INSUFFICIENT"):
        state.last_failure = f"model judged the {len(state.evidence)} evidence items insufficient"
        state.hypothesis.status = "UNCERTAIN"
        state.phase = AgentPhase.INVESTIGATE
        return state

    if llm is not None and state.evidence:
        text = _llm_text(
            llm, _VERIFY_SYSTEM,
            f"Claim: {state.hypothesis.claim}\n\nEvidence:\n{_format_evidence(_evidence_for_claim(state))}",
        )
        if text is not None:
            verdict = parse_verdict(text)
            state.hypothesis.status = verdict
            if verdict == "VERIFIED":
                state.hypothesis.confidence = 0.85
                state.phase = AgentPhase.UPDATE_GRAPH
            else:
                state.last_failure = f"verifier answered {verdict}"
                state.phase = AgentPhase.INVESTIGATE
            return state
        log.warning("LLM verify unavailable, falling back to heuristic")

    # Heuristic: need evidence that actually mentions the task's keywords.
    if state.evidence and _relevant(state):
        state.hypothesis.status = "VERIFIED"
        state.hypothesis.confidence = 0.8
        state.phase = AgentPhase.UPDATE_GRAPH
    else:
        state.last_failure = ("no evidence found" if not state.evidence
                              else "evidence does not mention the task's keywords")
        state.hypothesis.status = "UNCERTAIN"
        state.phase = AgentPhase.INVESTIGATE
    return state


def _file_of(source: str) -> str:
    return source.rsplit(":", 1)[0].replace("\\", "/")


def node_update_graph(state: AgentState, store=None) -> AgentState:
    """UPDATE_GRAPH: the provenance gate. Only grounded claims reach the graph."""
    from archon.verification.hallucination import FilterStatus, check_claim_grounded

    h = state.hypothesis
    if not h or h.status != "VERIFIED":
        state.phase = AgentPhase.IDENTIFY_UNKNOWNS
        return state

    result = check_claim_grounded(
        h.claim, [(e.source, e.content) for e in state.evidence],
        require_citation=state.require_citation,
    )
    if result.status != FilterStatus.PASSES:
        log.warning("✗ blocked by provenance gate: %s", result.reason)
        state.rejected.append(h.claim)
        state.last_failure = f"provenance gate: {result.reason}"
        h.status = "REJECTED"
        state.phase = AgentPhase.INVESTIGATE
        return state

    refs = ", ".join(result.provenance_found[:3])
    state.findings.append(f"{h.claim} [conf={h.confidence:.2f}] ({refs})")
    log.info("✓ task %d/%d verified (%s)", state.task_index + 1, len(state.tasks), refs)

    if store is not None:
        from archon.graph.neo4j_client import GraphEdge, GraphNode
        nid = f"finding::{state.task_index + 1}::{state.iteration}"
        store.upsert_node(GraphNode(
            id=nid, label="Hypothesis",
            properties={"claim": h.claim, "task": state.current_task},
            confidence=h.confidence, provenance=result.provenance_found[0],
        ))
        for i, ev in enumerate(state.evidence[:5]):
            eid = f"evidence::{nid}::{i}"
            store.upsert_node(GraphNode(
                id=eid, label="Evidence",
                properties={"source": ev.source, "content": ev.content[:200], "tool": ev.tool},
                confidence=0.9, provenance=ev.source,
            ))
            store.upsert_edge(GraphEdge(source_id=eid, target_id=nid, rel_type="SUPPORTS"))
        for f in {_file_of(e.source) for e in state.evidence[:8]}:
            if store.get_node(f) is not None:
                store.upsert_edge(GraphEdge(source_id=nid, target_id=f, rel_type="ABOUT"))

    state.phase = AgentPhase.IDENTIFY_UNKNOWNS
    return state


def node_identify_unknowns(state: AgentState, store=None,
                           max_iterations: int = 20) -> AgentState:
    """Advance past a verified task; finish when no tasks or no budget remain."""
    if state.hypothesis and state.hypothesis.status == "VERIFIED":
        state.task_index += 1
        state.retries = 0
        state.search_terms = []
        state.last_failure = ""

    if state.task_index >= len(state.tasks):
        state.phase = AgentPhase.COMPLETE
    elif state.iteration >= max_iterations:
        for t in state.tasks[state.task_index:]:
            if t not in state.unknowns:
                state.unknowns.append(t)
        state.phase = AgentPhase.COMPLETE
    else:
        state.phase = AgentPhase.PLAN
    return state


_TERMS_SYSTEM = (
    "You help search a Python codebase. Reply with 3-6 identifier names (functions, "
    "classes or variables) that are likely to appear in the code that answers the task, "
    "as a comma-separated list. No prose, no explanation."
)


def _suggest_search_terms(llm, task: str, repo_summary: str, reason: str) -> list[str]:
    """Ask the LLM for identifiers to search for. These only steer the search;
    they are never treated as evidence."""
    from archon.agent.evidence import _STOP
    text = _llm_text(
        llm, _TERMS_SYSTEM,
        f"Task: {task}\nPrevious attempt failed because: {reason}\n\nRepository:\n{repo_summary}",
    )
    if not text:
        return []
    terms: list[str] = []
    for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text):
        tl = t.lower()
        if tl not in _STOP and tl not in terms:
            terms.append(tl)
    return terms[:6]


def _evidence_for_claim(state: AgentState) -> list[Evidence]:
    """Evidence the claim actually cites (cheaper, stricter verification);
    all evidence when the claim cites nothing."""
    from archon.verification.hallucination import (
        _PROVENANCE_RE, _file_of as _hf, _line_of, _same_file)
    cited = _PROVENANCE_RE.findall(state.hypothesis.claim if state.hypothesis else "")
    if not cited:
        return state.evidence
    wanted = [(_hf(c), _line_of(c)) for c in cited]
    picked = [e for e in state.evidence
              if any(_same_file(_hf(e.source), wf) and _line_of(e.source) == wl
                     for wf, wl in wanted)]
    return picked or state.evidence


def node_investigate(state: AgentState, llm=None, repo_summary: str = "") -> AgentState:
    """INVESTIGATE: retry the task with a wider search, or give up on it."""
    state.retries += 1
    reason = state.last_failure or "no verdict"
    if state.retries > MAX_RETRIES_PER_TASK:
        log.warning("⚠ giving up on task %d/%d (%s): %s",
                    state.task_index + 1, len(state.tasks), reason, state.current_task)
        if state.current_task not in state.unknowns:
            state.unknowns.append(state.current_task)
        state.task_index += 1
        state.retries = 0
        state.search_terms = []
    else:
        if llm is not None:
            state.search_terms = _suggest_search_terms(llm, state.current_task,
                                                       repo_summary, reason)
        log.info("↻ retry task %d/%d — previous attempt failed: %s%s",
                 state.task_index + 1, len(state.tasks), reason,
                 f" | new search terms: {', '.join(state.search_terms)}" if state.search_terms else "")
    state.last_failure = ""
    state.hypothesis = None
    state.evidence = []
    state.phase = AgentPhase.PLAN
    return state


def node_complete(state: AgentState) -> AgentState:
    state.complete = True
    state.phase = AgentPhase.COMPLETE
    return state


# ── Routers ───────────────────────────────────────────────────────────────────

def route_after_verify(state: AgentState) -> str:
    if state.hypothesis and state.hypothesis.status == "VERIFIED":
        return "update_graph"
    return "investigate"


def route_after_update(state: AgentState) -> str:
    if state.hypothesis and state.hypothesis.status == "REJECTED":
        return "investigate"
    return "identify_unknowns"


def route_after_unknowns(state: AgentState, max_iterations: int = 20) -> str:
    return "complete" if state.phase == AgentPhase.COMPLETE else "plan"


# ── Graph builder ─────────────────────────────────────────────────────────────

def build_agent_graph(
    llm=None,
    harness=None,
    store=None,
    max_iterations: int = 20,
    ctx_engine=None,
    repo_root=None,
    repo_summary: str = "",
):
    """Build and compile the LangGraph StateGraph."""

    def wrap(fn):
        def _wrapped(state_dict):
            return fn(AgentState(**state_dict)).model_dump()
        return _wrapped

    def wrap_router(fn):
        def _wrapped(state_dict):
            return fn(AgentState(**state_dict))
        return _wrapped

    builder = StateGraph(dict)
    builder.add_node("plan", wrap(lambda s: node_plan(s, llm=llm, harness=harness,
                                                       max_iterations=max_iterations)))
    builder.add_node("act", wrap(lambda s: node_act(s, harness=harness, ctx_engine=ctx_engine,
                                                     repo_root=repo_root, store=store)))
    builder.add_node("observe", wrap(lambda s: node_observe(s, llm=llm)))
    builder.add_node("verify", wrap(lambda s: node_verify(s, llm=llm)))
    builder.add_node("update_graph", wrap(lambda s: node_update_graph(s, store=store)))
    builder.add_node("identify_unknowns", wrap(lambda s: node_identify_unknowns(
        s, store=store, max_iterations=max_iterations)))
    builder.add_node("investigate", wrap(lambda s: node_investigate(
        s, llm=llm, repo_summary=repo_summary)))
    builder.add_node("complete", wrap(node_complete))

    builder.set_entry_point("plan")
    builder.add_conditional_edges(
        "plan", wrap_router(lambda s: "complete" if s.complete else "act"),
        {"act": "act", "complete": "complete"})
    builder.add_edge("act", "observe")
    builder.add_edge("observe", "verify")
    builder.add_conditional_edges("verify", wrap_router(route_after_verify),
                                  {"update_graph": "update_graph", "investigate": "investigate"})
    builder.add_conditional_edges("update_graph", wrap_router(route_after_update),
                                  {"identify_unknowns": "identify_unknowns",
                                   "investigate": "investigate"})
    builder.add_conditional_edges("identify_unknowns",
                                  wrap_router(lambda s: route_after_unknowns(s, max_iterations)),
                                  {"complete": "complete", "plan": "plan"})
    builder.add_edge("investigate", "plan")
    builder.add_edge("complete", END)

    # each iteration uses up to ~7 graph steps; LangGraph's default limit is 25
    compiled = builder.compile()
    return compiled.with_config({"recursion_limit": max(25, max_iterations * 10 + 10)})
