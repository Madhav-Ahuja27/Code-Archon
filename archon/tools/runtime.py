"""Runtime tools: pytest runner and coverage.py."""

from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

log = logging.getLogger(__name__)


class TestResult(BaseModel):
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    duration: float = 0.0
    failures: list[str] = []


class CoverageResult(BaseModel):
    total_pct: float = 0.0
    per_module: dict[str, float] = {}


def run_pytest(
    path: str | Path,
    test_filter: Optional[str] = None,
    timeout: int = 60,
) -> TestResult:
    """Run pytest on `path`, return structured results."""
    cmd = [sys.executable, "-m", "pytest", str(path), "--tb=no", "-q",
           "--no-header", "--json-report", "--json-report-file=/tmp/archon_pytest.json"]
    if test_filter:
        cmd += ["-k", test_filter]
    try:
        subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
        report_path = Path("/tmp/archon_pytest.json")
        if report_path.exists():
            data = json.loads(report_path.read_text())
            summary = data.get("summary", {})
            failures = [
                f"{t['nodeid']}: {t.get('longrepr','')[:200]}"
                for t in data.get("tests", [])
                if t.get("outcome") in ("failed", "error")
            ]
            return TestResult(
                passed=summary.get("passed", 0),
                failed=summary.get("failed", 0),
                errors=summary.get("errors", 0),
                skipped=summary.get("skipped", 0),
                duration=data.get("duration", 0.0),
                failures=failures,
            )
    except subprocess.TimeoutExpired:
        log.warning("pytest timed out after %ds", timeout)
    except Exception as e:
        log.warning("run_pytest error: %s", e)

    # Fallback: run without json-report
    try:
        cmd_simple = [sys.executable, "-m", "pytest", str(path), "--tb=no", "-q"]
        if test_filter:
            cmd_simple += ["-k", test_filter]
        result = subprocess.run(cmd_simple, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
        output = result.stdout + result.stderr
        passed = output.count(" passed")
        failed = output.count(" failed")
        return TestResult(passed=passed, failed=failed)
    except Exception as e:
        log.warning("fallback pytest error: %s", e)
    return TestResult()


def run_coverage(path: str | Path, timeout: int = 90) -> CoverageResult:
    """Run coverage.py on a path, return per-module percentages."""
    p = Path(path)
    try:
        subprocess.run(
            [sys.executable, "-m", "coverage", "run", "--source", str(p),
             "-m", "pytest", str(p), "--tb=no", "-q"],
            capture_output=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        result = subprocess.run(
            [sys.executable, "-m", "coverage", "json", "-o", "/tmp/archon_cov.json"],
            capture_output=True, encoding="utf-8", errors="replace", timeout=30,
        )
        cov_path = Path("/tmp/archon_cov.json")
        if cov_path.exists():
            data = json.loads(cov_path.read_text())
            total = data.get("totals", {}).get("percent_covered", 0.0)
            per_module = {
                f: v.get("summary", {}).get("percent_covered", 0.0)
                for f, v in data.get("files", {}).items()
            }
            return CoverageResult(total_pct=total, per_module=per_module)
    except Exception as e:
        log.warning("run_coverage error: %s", e)
    return CoverageResult()
