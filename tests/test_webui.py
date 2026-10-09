"""Regression tests for the local investigation launcher UI."""
from __future__ import annotations

from pathlib import Path

from archon import webui


def test_cli_output_updates_visible_phase() -> None:
    assert webui._phase_for("Parsing repository...", "Starting") == "Repository scan"
    assert webui._phase_for("Graph store: in-memory", "Starting") == "Building code graph"
    assert webui._phase_for("Running agent loop...", "Planning") == "Investigating"
    assert webui._phase_for("Documentation written → demo-output", "Investigating") == "Complete"
    assert webui._phase_for("some unrelated output", "Investigating") == "Investigating"


def test_public_run_omits_process_and_command() -> None:
    run = {
        "id": "test-id",
        "status": "running",
        "started_epoch": 10.0,
        "finished_epoch": None,
        "output_path": Path("demo-output"),
        "logs": ["first", "second"],
        "process": object(),
        "command": ["python", "private argument"],
    }
    result = webui._public_run(run)
    assert result["output_path"] == "demo-output"
    assert result["logs"] == ["first", "second"]
    assert "process" not in result
    assert "command" not in result
    assert result["elapsed_seconds"] >= 0


def test_launcher_html_contains_setup_and_live_monitor() -> None:
    html = (Path(webui.__file__).parent / "ui" / "launcher.html").read_text(encoding="utf-8")
    for marker in (
        "Repository folder",
        "Investigation goal",
        "Output folder",
        "Iteration limit",
        "LLM-assisted",
        "Heuristic",
        "Investigation monitor",
        "Execution log",
        "/api/investigations",
        "/api/runs/",
    ):
        assert marker in html
