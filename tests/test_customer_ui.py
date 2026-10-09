"""Customer-facing workspace UI regression tests."""
from pathlib import Path

from archon import webui


def test_customer_workspace_contains_user_flow() -> None:
    html = (Path(webui.__file__).parent / "ui" / "product.html").read_text(encoding="utf-8")
    for marker in (
        "Your codebase, understood.",
        "New investigation",
        "What would you like to understand?",
        "Understand routing",
        "Your investigations",
        "Ready to explore",
        "/api/investigations",
        "/api/runs",
        "/api/open?run=",
    ):
        assert marker in html


def test_customer_and_developer_pages_are_separate() -> None:
    source = Path(webui.__file__).read_text(encoding="utf-8")
    assert 'path == "/" or path == "/app"' in source
    assert 'path == "/dev"' in source
    assert 'product.html' in source
    assert 'launcher.html' in source
