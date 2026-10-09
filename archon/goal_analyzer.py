"""Goal Analyzer — converts free-text objective into structured InvestigationGoal.

Uses make_llm() (Groq / Anthropic / OpenAI) when available.
Falls back to keyword-based analysis when offline / no API key.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Optional

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class InvestigationGoal(BaseModel):
    objective: str
    focus_modules: list[str] = Field(default_factory=list)
    investigation_tasks: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)


# ── Keyword-based fallback (no LLM required) ─────────────────────────────────

_TASK_PATTERNS = {
    "auth":    ["trace authentication flow", "identify login functions",
                "map session management"],
    "api":     ["enumerate API endpoints", "trace request handling",
                "map route definitions"],
    "db":      ["identify database models", "map query patterns",
                "trace connection lifecycle"],
    "test":    ["audit test coverage", "identify untested modules"],
    "dep":     ["map external dependencies", "identify import graph"],
    "route":   ["map routing system", "trace URL dispatch", "identify view functions"],
    "session": ["trace session lifecycle", "map session storage"],
}

_DEFAULT_TASKS = [
    "map module structure",
    "identify entry points",
    "trace call graph",
    "document public API",
]

_SYSTEM_PROMPT = """You are a software archaeology assistant.
Convert the investigation objective into a structured JSON plan.
Respond ONLY with valid JSON — no markdown fences, no preamble.
The user message may include a 'Repository' section describing the codebase. The codebase is a Python project: every task must be answerable by reading its Python source, should name real modules or classes from the Repository section where possible, and must not mention other languages, frameworks or file types.
Schema:
{
  "objective": "<restate objective concisely>",
  "focus_modules": ["<module names if mentioned, else empty list>"],
  "investigation_tasks": ["<3-5 concrete tasks>"],
  "success_criteria": ["<2-3 measurable success criteria>"]
}"""


def _keyword_analyze(objective: str) -> InvestigationGoal:
    obj_lower = objective.lower()
    tasks: list[str] = []
    for keyword, task_list in _TASK_PATTERNS.items():
        if keyword in obj_lower:
            tasks.extend(task_list)
    if not tasks:
        tasks = list(_DEFAULT_TASKS)
    py_refs = re.findall(r"\b(\w+\.py|\w+module|\w+_\w+)\b", obj_lower)
    modules = list(dict.fromkeys(py_refs))
    return InvestigationGoal(
        objective=objective,
        focus_modules=modules,
        investigation_tasks=list(dict.fromkeys(tasks)),
        success_criteria=[
            "All identified modules documented with confidence ≥ 0.7",
            "Zero hallucinated claims in final graph",
            "Call chain traced from entry points",
        ],
    )


def _llm_analyze(objective: str, llm, repo_summary: str = "") -> InvestigationGoal:
    from langchain_core.messages import HumanMessage, SystemMessage
    try:
        messages = [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=f"Objective: {objective}"
                         + (f"\n\nRepository:\n{repo_summary}" if repo_summary else "")),
        ]
        response = llm.invoke(messages)
        text = response.content if hasattr(response, "content") else str(response)
        # Strip any accidental markdown fences
        text = re.sub(r"```(?:json)?", "", text).strip().strip("`").strip()
        data = json.loads(text)
        return InvestigationGoal(**data)
    except Exception as e:
        log.warning("LLM goal analysis failed (%s) — falling back to keyword", e)
        return _keyword_analyze(objective)


class GoalAnalyzer:
    """Converts free-text objective into InvestigationGoal."""

    def __init__(self, llm=None):
        self._llm = llm

    def analyze(self, objective: str, repo_summary: str = "") -> InvestigationGoal:
        if self._llm:
            return _llm_analyze(objective, self._llm, repo_summary)
        return _keyword_analyze(objective)


def make_goal_analyzer(use_llm: bool = True) -> GoalAnalyzer:
    """Factory — wires Groq LLM if available, else keyword-only."""
    if not use_llm:
        return GoalAnalyzer(llm=None)
    try:
        from archon.llm import make_llm
        llm = make_llm()
        return GoalAnalyzer(llm=llm)
    except Exception as e:
        log.warning("Could not create LLM (%s) — using keyword analyzer", e)
        return GoalAnalyzer(llm=None)
