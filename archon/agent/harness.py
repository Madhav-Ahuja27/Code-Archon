"""Agent Harness — enforces tool permissions, call limits, and recovery policy."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

log = logging.getLogger(__name__)


class ToolNotPermittedError(Exception):
    pass


class ToolCallLimitError(Exception):
    pass


@dataclass
class HarnessConfig:
    allowed_tools: set[str] = field(default_factory=lambda: {
        "ast_analysis", "radon", "semgrep", "pytest", "coverage",
        "ripgrep", "git_log", "git_blame",
    })
    call_limit_per_tool: int = 5
    require_evidence_before_promote: bool = True
    recovery_strategy: str = "REPLAN"   # REPLAN | RETRY | SKIP
    max_iterations: int = 20


@dataclass
class ToolCall:
    tool: str
    input: dict[str, Any]
    output: Any = None
    error: Optional[str] = None
    source: str = ""   # "file.py:line"


class Harness:
    """Wraps every tool call: permission check, call-limit, logging, recovery."""

    def __init__(self, config: Optional[HarnessConfig] = None):
        self._config = config or HarnessConfig()
        self._call_counts: dict[str, int] = {}
        self._log: list[ToolCall] = []

    # ── Permission / limit checks ─────────────────────────────────────────────

    def _check(self, tool: str) -> None:
        if tool not in self._config.allowed_tools:
            raise ToolNotPermittedError(
                f"Tool '{tool}' not in allowlist: {self._config.allowed_tools}"
            )
        count = self._call_counts.get(tool, 0)
        if count >= self._config.call_limit_per_tool:
            raise ToolCallLimitError(
                f"Tool '{tool}' call limit ({self._config.call_limit_per_tool}) reached"
            )

    # ── Public API ────────────────────────────────────────────────────────────

    def call(self, tool: str, fn: Callable, **kwargs) -> ToolCall:
        """Execute a tool function with harness enforcement."""
        self._check(tool)
        tc = ToolCall(tool=tool, input=kwargs)
        try:
            from archon.observability.events import emit_event
            emit_event("tool_started", stage="ACT", message=f"{tool} started",
                       details={"tool": tool, "input": {k: str(v)[:1500] for k, v in kwargs.items()}})
        except Exception:
            pass
        try:
            result = fn(**kwargs)
            tc.output = result
            tc.source = kwargs.get("source", "")
            try:
                from archon.observability.events import emit_event
                emit_event("tool_completed", stage="ACT", message=f"{tool} completed",
                           details={"tool": tool, "source": tc.source,
                                    "output": str(result)[:5000], "error": ""})
            except Exception:
                pass
        except (ToolNotPermittedError, ToolCallLimitError):
            raise
        except Exception as e:
            tc.error = str(e)
            try:
                from archon.observability.events import emit_event
                emit_event("tool_failed", stage="ACT", message=f"{tool} failed",
                           details={"tool": tool, "input": {k: str(v)[:1500] for k, v in kwargs.items()},
                                    "error": str(e)[:3000]})
            except Exception:
                pass
            log.warning("Tool '%s' error: %s — recovery: %s",
                        tool, e, self._config.recovery_strategy)
        finally:
            self._call_counts[tool] = self._call_counts.get(tool, 0) + 1
            self._log.append(tc)
        return tc

    def execute_default_tool(self, state) -> Optional[dict]:
        """Run a default no-op tool for the agent loop (returns synthetic evidence)."""
        tool = "ast_analysis"
        if tool not in self._config.allowed_tools:
            return None
        count = self._call_counts.get(tool, 0)
        if count >= self._config.call_limit_per_tool:
            return None
        self._call_counts[tool] = count + 1
        result = {
            "tool": tool,
            "source": f"synthetic:iter_{state.iteration}",
            "output": f"Analyzed goal: {state.goal}",
        }
        try:
            from archon.observability.events import emit_event
            emit_event("tool_started", stage="ACT", message=f"{tool} started",
                       details={"tool": tool, "input": {}, "synthetic": True})
            emit_event("tool_completed", stage="ACT", message=f"{tool} completed",
                       details={"tool": tool, "source": result["source"],
                                "output": result["output"], "synthetic": True})
        except Exception:
            pass
        self._log.append(ToolCall(tool=tool, input={}, output=result["output"],
                                   source=result["source"]))
        return result

    def begin_iteration(self) -> None:
        """Reset per-tool call counts (keeps the log). Limits apply per iteration."""
        self._call_counts.clear()

    def recovery_action(self, tool: str) -> str:
        return self._config.recovery_strategy

    # ── Inspection ────────────────────────────────────────────────────────────

    def call_log(self) -> list[ToolCall]:
        return list(self._log)

    def call_count(self, tool: str) -> int:
        return self._call_counts.get(tool, 0)

    def reset_counts(self) -> None:
        self._call_counts.clear()
        self._log.clear()
