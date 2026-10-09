"""Regression tests for live observability UI and event tracing."""
from pathlib import Path

from archon.observability.events import emit_event, read_events
from archon import webui


def test_live_dashboard_exposes_real_operational_panels() -> None:
    page = (Path(__file__).parents[1] / "archon" / "observability" / "dashboard.html").read_text(encoding="utf-8")
    for marker in (
        "Investigation event stream",
        "Search events, files, tools…",
        "Filter event types",
        "Raw process output",
        "Infrastructure",
        "Docker containers",
        "View last 100 log lines",
        "/api/infrastructure/container-logs",
        "/api/infrastructure",
        "/api/observability/",
        "Neo4j",
        "Redis",
    ):
        assert marker in page


def test_web_server_wires_live_dashboard_and_telemetry_apis() -> None:
    source = Path(webui.__file__).read_text(encoding="utf-8")
    assert 'path == "/live"' in source
    assert 'path == "/api/infrastructure"' in source
    assert 'r"/api/observability/([a-f0-9-]+)/events"' in source
    assert 'child_env["ARCHON_EVENT_LOG"]' in source


def test_event_sink_writes_readable_jsonl_records(monkeypatch, tmp_path) -> None:
    target = tmp_path / "trace.jsonl"
    monkeypatch.setenv("ARCHON_EVENT_LOG", str(target))
    emit_event("node_started", stage="PLAN", message="Plan started", details={"iteration": 1})
    emit_event("node_completed", stage="PLAN", message="Plan finished", details={"iteration": 1})
    events = read_events(target)
    assert [event["event"] for event in events] == ["node_started", "node_completed"]
    assert events[0]["details"]["iteration"] == 1


def test_customer_progress_includes_actual_event_timeline_and_service_snapshot() -> None:
    page = (Path(__file__).parents[1] / "archon" / "ui" / "product.html").read_text(encoding="utf-8")
    for marker in (
        "Live activity",
        "Agent stages",
        "Evidence and findings",
        "Full systems view",
        "/api/observability/",
        "/api/infrastructure",
        "No event does not mean the step did not happen",
    ):
        assert marker in page


def test_customer_ui_keeps_navigation_available_on_mobile_and_supports_modal_keyboard_access() -> None:
    page = (Path(__file__).parents[1] / "archon" / "ui" / "product.html").read_text(encoding="utf-8")
    assert 'aria-label="Workspace navigation"' in page
    assert 'id="nav-overview"' in page
    assert '.sidebar .navlabel,.bottom{display:none}' in page
    assert '.sidebar .nav{display:flex' in page
    assert "e.key==='Escape'" in page
    assert "if(e.key==='Tab')" in page
    assert "modalReturnFocus.focus()" in page
    assert "prefers-reduced-motion:reduce" in page


def test_frontend_pages_include_responsive_accessibility_and_trace_controls() -> None:
    root = Path(__file__).parents[1]
    launcher = (root / "archon" / "ui" / "launcher.html").read_text(encoding="utf-8")
    live = (root / "archon" / "observability" / "dashboard.html").read_text(encoding="utf-8")
    assert ":focus-visible" in launcher and "prefers-reduced-motion:reduce" in launcher
    assert ".path-row{flex-wrap:wrap}" in launcher
    assert 'id="toggle-refresh"' in live and 'id="export-trace"' in live
    assert "Auto-refresh paused" in live
    assert "JSON.stringify(payload,null,2)" in live
    assert "data may be stale" in live
    assert "lastSuccessAt" in live
    assert ":focus-visible" in live and "prefers-reduced-motion:reduce" in live


def test_live_trace_can_group_events_and_copy_individual_event_payloads() -> None:
    page = (Path(__file__).parents[1] / "archon" / "observability" / "dashboard.html").read_text(encoding="utf-8")
    for marker in (
        'id="toggle-grouping"',
        "let groupEventsByStage=true",
        'class="eventgroup"',
        "Unstaged events",
        "Copy event JSON",
        "navigator.clipboard.writeText(JSON.stringify(item,null,2))",
    ):
        assert marker in page
