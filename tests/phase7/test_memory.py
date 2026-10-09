"""Phase 7 — Memory Layer (SQLite + Redis) tests.

Gate: all 8 pass before Phase 8 begins.
"""

from __future__ import annotations

import pytest

from archon.memory.sqlite_store import SQLiteStore
from archon.memory.redis_store import make_redis_store, _TTL_SECONDS


# ── SQLite fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def db():
    """Fresh in-memory SQLite store per test."""
    store = SQLiteStore(db_path=":memory:")
    yield store
    store.close()


def _snap(iteration: int) -> dict:
    return {
        "goal": "test goal",
        "iteration": iteration,
        "phase": "PLAN",
        "findings": [],
        "evidence": [],
        "unknowns": [],
        "complete": False,
    }


# ── Test 1: SQLite save and load round-trip ───────────────────────────────────

def test_sqlite_save_and_load(db):
    db.create_session("s1", "understand auth module")
    snap = _snap(1)
    db.save_iteration("s1", snap)
    loaded = db.load_session("s1")
    assert len(loaded) == 1
    assert loaded[0]["iteration"] == 1
    assert loaded[0]["goal"] == "test goal"


# ── Test 2: multiple iterations saved and loaded in order ────────────────────

def test_sqlite_multiple_iterations(db):
    db.create_session("s2", "trace call graph")
    for i in range(1, 6):
        db.save_iteration("s2", _snap(i))
    loaded = db.load_session("s2")
    assert len(loaded) == 5
    iterations = [l["iteration"] for l in loaded]
    assert iterations == [1, 2, 3, 4, 5]


# ── Test 3: evidence query by module_id ──────────────────────────────────────

def test_sqlite_evidence_query(db):
    db.create_session("s3", "test")
    db.save_evidence("s3", "auth.py", "auth.py:14", "def hash_password", supports=True)
    db.save_evidence("s3", "auth.py", "auth.py:22", "def verify_password", supports=True)
    db.save_evidence("s3", "api.py",  "api.py:5",   "def login", supports=True)

    auth_evidence = db.get_evidence_for_module("auth.py")
    assert len(auth_evidence) == 2
    sources = {e["source"] for e in auth_evidence}
    assert "auth.py:14" in sources
    assert "auth.py:22" in sources

    api_evidence = db.get_evidence_for_module("api.py")
    assert len(api_evidence) == 1


# ── Test 4: Redis save → key exists ──────────────────────────────────────────

def test_redis_save_summary():
    store = make_redis_store()  # mock if Redis not running
    store.save_repo_summary("abc123", {"modules": 5, "verified": 3})
    result = store.load_repo_summary("abc123")
    assert result is not None


# ── Test 5: Redis load → same dict as saved ───────────────────────────────────

def test_redis_load_summary():
    store = make_redis_store()
    payload = {"modules": 12, "findings": ["auth module documented"], "score": 0.87}
    store.save_repo_summary("def456", payload)
    loaded = store.load_repo_summary("def456")
    assert loaded == payload


# ── Test 6: Redis missing key → None, no crash ───────────────────────────────

def test_redis_missing_key():
    store = make_redis_store()
    result = store.load_repo_summary("nonexistent_repo_hash_xyz")
    assert result is None


# ── Test 7: Redis TTL ≤ 30 days ──────────────────────────────────────────────

def test_redis_ttl_set():
    store = make_redis_store()
    store.save_repo_summary("ttl_test", {"x": 1})
    ttl = store.ttl("ttl_test")
    assert 0 < ttl <= _TTL_SECONDS


# ── Test 8: cross-session resume loads prior summary ─────────────────────────

def test_cross_session_resume():
    """New session for same repo picks up prior summary."""
    store = make_redis_store()
    repo_hash = "resume_test_repo_001"
    prior_summary = {
        "modules_found": 8,
        "entry_points": ["main.py::main"],
        "confidence_avg": 0.75,
    }
    # Session 1 saves summary
    store.save_repo_summary(repo_hash, prior_summary)

    # Session 2 loads it (simulated by just calling load on same store)
    resumed = store.load_repo_summary(repo_hash)
    assert resumed is not None
    assert resumed["modules_found"] == 8
    assert resumed["confidence_avg"] == 0.75
