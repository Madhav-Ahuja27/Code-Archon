"""SQLite session memory — stores iteration snapshots and evidence cache."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS investigation_sessions (
    session_id TEXT PRIMARY KEY,
    goal TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS iteration_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    iteration INTEGER NOT NULL,
    state_snapshot TEXT NOT NULL,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES investigation_sessions(session_id)
);

CREATE TABLE IF NOT EXISTS evidence_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    supports INTEGER NOT NULL DEFAULT 1,  -- 1=supports, 0=contradicts
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


class SQLiteStore:
    """Per-session investigation history stored in SQLite."""

    def __init__(self, db_path: str | Path = ":memory:"):
        self._path = str(db_path)
        if self._path != ":memory:":
            Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ── Session management ────────────────────────────────────────────────────

    def create_session(self, session_id: str, goal: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO investigation_sessions (session_id, goal) VALUES (?, ?)",
            (session_id, goal),
        )
        self._conn.commit()

    def session_exists(self, session_id: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM investigation_sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        return row is not None

    # ── Iteration log ─────────────────────────────────────────────────────────

    def save_iteration(self, session_id: str, state_snapshot: dict) -> None:
        iteration = state_snapshot.get("iteration", 0)
        self._conn.execute(
            "INSERT INTO iteration_log (session_id, iteration, state_snapshot) VALUES (?, ?, ?)",
            (session_id, iteration, json.dumps(state_snapshot)),
        )
        self._conn.commit()

    def load_session(self, session_id: str) -> list[dict]:
        rows = self._conn.execute(
            "SELECT state_snapshot FROM iteration_log WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
        return [json.loads(r["state_snapshot"]) for r in rows]

    def iteration_count(self, session_id: str) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) AS c FROM iteration_log WHERE session_id = ?", (session_id,)
        ).fetchone()
        return row["c"]

    # ── Evidence cache ────────────────────────────────────────────────────────

    def save_evidence(
        self,
        session_id: str,
        module_id: str,
        source: str,
        content: str,
        supports: bool = True,
    ) -> None:
        self._conn.execute(
            "INSERT INTO evidence_cache (session_id, module_id, source, content, supports) "
            "VALUES (?, ?, ?, ?, ?)",
            (session_id, module_id, source, content, int(supports)),
        )
        self._conn.commit()

    def get_evidence_for_module(self, module_id: str) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM evidence_cache WHERE module_id = ? ORDER BY id",
            (module_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self._conn.close()
