"""Static analysis tools: AST, radon complexity, semgrep."""

from __future__ import annotations

import ast
import logging
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel

log = logging.getLogger(__name__)


class StaticFinding(BaseModel):
    file: str
    line: int
    kind: str       # "complexity" | "smell" | "security" | "error"
    message: str
    severity: str = "info"


def run_ast_analysis(file_path: str | Path) -> list[dict[str, Any]]:
    """Parse file with ast and return function/class node list."""
    path = Path(file_path)
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (OSError, SyntaxError) as e:
        return [{"error": str(e), "file": str(path)}]

    nodes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            nodes.append({
                "kind": "function",
                "name": node.name,
                "line": node.lineno,
                "file": str(path),
            })
        elif isinstance(node, ast.ClassDef):
            nodes.append({
                "kind": "class",
                "name": node.name,
                "line": node.lineno,
                "file": str(path),
            })
    return nodes


def run_radon(file_path: str | Path) -> list[StaticFinding]:
    """Compute cyclomatic complexity per function via radon."""
    path = Path(file_path)
    findings: list[StaticFinding] = []
    try:
        from radon.complexity import cc_visit
        source = path.read_text(encoding="utf-8", errors="replace")
        results = cc_visit(source)
        for r in results:
            grade = getattr(r, "letter", getattr(r, "rank", "?"))
            findings.append(StaticFinding(
                file=str(path),
                line=r.lineno,
                kind="complexity",
                message=f"{r.name}: CC={r.complexity} ({grade})",
                severity="warning" if r.complexity > 5 else "info",
            ))
    except ImportError:
        findings.append(StaticFinding(
            file=str(path), line=0, kind="error",
            message="radon not installed", severity="error",
        ))
    except Exception as e:
        findings.append(StaticFinding(
            file=str(path), line=0, kind="error",
            message=str(e), severity="error",
        ))
    return findings


def run_semgrep(repo_path: str | Path, rules: str = "auto") -> list[StaticFinding]:
    """Run semgrep on a path, return structured findings."""
    path = Path(repo_path)
    findings: list[StaticFinding] = []
    try:
        result = subprocess.run(
            ["semgrep", "--config", rules, "--json", str(path)],
            capture_output=True, encoding="utf-8", errors="replace", timeout=60,
        )
        if result.returncode not in (0, 1):
            # semgrep exits 1 when findings exist — that's fine
            log.warning("semgrep stderr: %s", result.stderr[:200])
            return findings
        import json
        data = json.loads(result.stdout)
        for item in data.get("results", []):
            findings.append(StaticFinding(
                file=item.get("path", ""),
                line=item.get("start", {}).get("line", 0),
                kind="security",
                message=item.get("extra", {}).get("message", ""),
                severity=item.get("extra", {}).get("severity", "warning").lower(),
            ))
    except FileNotFoundError:
        log.info("semgrep not installed — skipping")
    except Exception as e:
        log.warning("semgrep error: %s", e)
    return findings
