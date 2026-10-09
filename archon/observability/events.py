"""Best-effort JSONL event sink for live investigation traces.

Instrumentation is observational only: event write failures are swallowed so they can
never change investigation behavior. Set ARCHON_EVENT_LOG to enable persistence.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_LOCK = threading.Lock()
_MAX_TEXT = 12_000


def emit_event(event: str, *, stage: str = "", message: str = "", details: dict[str, Any] | None = None) -> None:
    """Append one structured event; never raise into the analysis pipeline."""
    target = os.environ.get("ARCHON_EVENT_LOG", "").strip()
    if not target:
        return
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": str(event)[:120],
        "stage": str(stage)[:120],
        "message": str(message)[:_MAX_TEXT],
        "details": details or {},
    }
    try:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(payload, ensure_ascii=False, default=str) + "\n"
        with _LOCK:
            with path.open("a", encoding="utf-8") as stream:
                stream.write(line)
    except Exception:
        # Observability must not interfere with an investigation.
        return


def read_events(path: str | Path, limit: int = 600) -> list[dict[str, Any]]:
    """Read the most recent well-formed events from a run's JSONL trace."""
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]
    except OSError:
        return []
    events = []
    for line in lines:
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                events.append(item)
        except (json.JSONDecodeError, TypeError):
            continue
    return events
