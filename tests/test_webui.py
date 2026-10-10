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


def test_diagnostics_extract_real_cli_counters() -> None:
    logs = [
        "✓ Parsed: 12 modules, 44 functions, 1 errors",
        "✓ Edges: 8 calls, 10 imports, 2 inherits",
        "✓ Graph: 25 nodes",
        "✓ Index: 70 chunks (vector backend: hash)",
        "✓ Goal decomposed into 4 tasks",
        "✓ Complete after 3 iterations",
        "  Verified findings : 2",
        "  Blocked by gate   : 1",
        "  Unresolved tasks  : 5",
    ]
    assert webui._diagnostics(logs) == {
        "modules": 12,
        "functions": 44,
        "parse_errors": 1,
        "call_edges": 8,
        "import_edges": 10,
        "inheritance_edges": 2,
        "graph_nodes": 25,
        "index_chunks": 70,
        "goal_tasks": 4,
        "iterations_used": 3,
        "verified_findings": 2,
        "rejected_claims": 1,
        "unresolved_tasks": 5,
    }


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
        "Advanced developer controls",
        "Keep existing Neo4j graph",
        "Explicit investigation tasks",
        "Cancel investigation",
        "Rerun with same configuration",
        "Index / graph diagnostics",
        "Built-in presets",
        "Saved in this browser",
        "Graph & index inspector",
        "LLM provider override",
        "Retrieval top-k",
        "Context token budget",
        "Tool calls per tool / iteration",
        "Evidence items per task",
    ):
        assert marker in html



def test_dev_tuning_controls_are_wired_to_cli_and_diagnostics_artifact() -> None:
    root = Path(webui.__file__).parents[1]
    cli = (root / "archon" / "cli.py").read_text(encoding="utf-8")
    evidence = (root / "archon" / "agent" / "evidence.py").read_text(encoding="utf-8")
    loop = (root / "archon" / "agent" / "loop.py").read_text(encoding="utf-8")
    server = Path(webui.__file__).read_text(encoding="utf-8")
    for option in (
        "--provider", "--model", "--retrieval-top-k", "--context-tokens",
        "--tool-call-limit", "--evidence-limit", "--prompt-evidence-limit",
        "archon-diagnostics.json", "parse_errors", "external_dependencies",
    ):
        assert option in cli
    assert "ARCHON_RETRIEVAL_TOP_K" in evidence
    assert "ARCHON_MAX_EVIDENCE" in evidence
    assert "ARCHON_PROMPT_EVIDENCE_ITEMS" in loop
    assert "/inspector" in server


def test_send_ignores_disconnected_client() -> None:
    class BrokenWriter:
        def write(self, body: bytes) -> None:
            raise ConnectionAbortedError("client disconnected")

    class DisconnectedHandler:
        wfile = BrokenWriter()

        def send_response(self, status: int) -> None:
            pass

        def send_header(self, name: str, value: str) -> None:
            pass

        def end_headers(self) -> None:
            pass

    # A dropped browser connection should not trigger a second HTTP response.
    webui.Handler._send(DisconnectedHandler(), 200, {"ok": True})
