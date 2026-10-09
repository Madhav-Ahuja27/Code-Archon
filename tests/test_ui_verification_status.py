"""Verification labels must preserve uncertainty instead of hiding unsupported claims."""
from pathlib import Path

from archon.ui_export import _task_verification


def test_task_without_verified_finding_is_explicitly_not_verified() -> None:
    result = _task_verification("Does the service use Redis?", False, set())
    assert result["status"] == "NOT VERIFIED"
    assert result["verification_label"] == "NOT VERIFIED"
    assert "unknown, not false" in result["status_detail"]


def test_attempted_task_without_verified_answer_is_unresolved_and_not_verified() -> None:
    result = _task_verification("Trace authentication", False, {"Trace authentication"})
    assert result["status"] == "UNRESOLVED"
    assert result["verification_label"] == "NOT VERIFIED"
    assert "no verified conclusion" in result["status_detail"]


def test_task_with_verified_finding_is_not_mislabeled() -> None:
    result = _task_verification("Trace routing", True, set())
    assert result["status"] == "VERIFIED"
    assert result["verification_label"] == "VERIFIED"


def test_generated_dashboard_has_a_dedicated_not_verified_panel() -> None:
    root = Path(__file__).parents[1]
    template = (root / "archon" / "ui" / "template.html").read_text(encoding="utf-8")
    exporter = (root / "archon" / "ui_export.py").read_text(encoding="utf-8")
    assert 'id="notVerifiedList"' in template
    assert 'id="notVerifiedCount"' in template
    assert 'id="findingSearch"' in template
    assert 'id="findingStatus"' in template
    assert 'function renderFindings()' in template
    assert '"not_verified": not_verified' in exporter
    assert 'No evidence supports a verified conclusion yet' in template


def test_findings_have_clickable_source_lines_and_explicit_provenance_gaps() -> None:
    root = Path(__file__).parents[1]
    template = (root / "archon" / "ui" / "template.html").read_text(encoding="utf-8")
    assert "function sourceRefFor(f)" in template
    assert 'data-source="'+"'"+'+esc(ref)' in template
    assert "function openEvidenceGap(title,reason)" in template
    assert "No source content has been invented." in template
    assert "No embedded source-line window is available" in template
    assert "data-gap-title" in template
