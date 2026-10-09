"""Phase 3 — Context Engine (BM25 + Vector Retrieval) tests.

Gate: all 8 pass before Phase 4 begins.
"""

from __future__ import annotations

import pytest

from archon.retrieval.bm25 import BM25Index, Chunk
from archon.retrieval.vector_store import ContextEngine, VectorStore


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_chunks(n: int = 10) -> list[Chunk]:
    return [
        Chunk(id=f"mod::fn_{i}", text=f"function number {i} does task_{i}",
              file_path="mod.py", line_start=i * 10, line_end=i * 10 + 5)
        for i in range(n)
    ]


def _auth_chunks() -> list[Chunk]:
    return [
        Chunk(id="auth::login", text="authentication login verify password user",
              file_path="auth.py", line_start=1, line_end=10),
        Chunk(id="api::routes", text="HTTP routing get post request response endpoint",
              file_path="api.py", line_start=1, line_end=20),
        Chunk(id="db::connect", text="database connection pool query cursor",
              file_path="db.py", line_start=1, line_end=15),
    ]


def _fresh_vs(chunks=None) -> VectorStore:
    """Each call returns a fully isolated ephemeral VectorStore."""
    vs = VectorStore(use_hash_embed=True)
    if chunks:
        vs.add_chunks(chunks)
    return vs


# ── Test 1: BM25 index builds ─────────────────────────────────────────────────

def test_bm25_index_builds():
    idx = BM25Index()
    idx.build(_make_chunks(10))
    assert idx.size() == 10


# ── Test 2: BM25 returns relevant result ─────────────────────────────────────

def test_bm25_returns_relevant():
    idx = BM25Index()
    idx.build(_auth_chunks())
    results = idx.query("authentication", top_k=3)
    assert len(results) > 0
    assert results[0].id == "auth::login"


# ── Test 3: vector store embeds chunks ────────────────────────────────────────

def test_vector_store_embeds():
    vs = _fresh_vs(_auth_chunks())
    assert vs.count() == 3


# ── Test 4: vector search returns result with provenance ─────────────────────

def test_vector_search_relevant():
    vs = _fresh_vs(_auth_chunks())
    results = vs.query("password verification", top_k=3)
    assert len(results) > 0
    for r in results:
        assert r.file_path != ""
        assert r.id != ""


# ── Test 5: hybrid deduplicates same chunk ────────────────────────────────────

def test_hybrid_deduplicates():
    chunks = _auth_chunks()
    idx = BM25Index()
    idx.build(chunks)
    vs = _fresh_vs(chunks)
    engine = ContextEngine(idx, vs, max_tokens=6000)
    results = engine.query("authentication login", top_k=5)
    ids = [r.id for r in results]
    assert len(ids) == len(set(ids))


# ── Test 6: context window respects token budget ──────────────────────────────

def test_context_window_token_budget():
    chunks = [
        Chunk(id=f"mod::fn_{i}", text="x " * 500,
              file_path="mod.py", line_start=0, line_end=0)
        for i in range(20)
    ]
    idx = BM25Index()
    idx.build(chunks)
    vs = _fresh_vs(chunks)
    engine = ContextEngine(idx, vs, max_tokens=6000)
    results = engine.query("x", top_k=20)
    context = engine.build_context_window(results)
    # 6000 tokens * 4 chars/token = 24000 chars budget
    assert len(context) <= 24000 + 500


# ── Test 7: empty BM25 + empty VS returns empty list ─────────────────────────

def test_empty_repo_no_crash():
    idx = BM25Index()
    idx.build([])           # explicitly empty
    vs = _fresh_vs([])      # explicitly empty
    engine = ContextEngine(idx, vs)
    results = engine.query("anything", top_k=5)
    assert results == []


# ── Test 8: every chunk from parse result has provenance ─────────────────────

def test_chunk_has_provenance():
    from pathlib import Path
    from archon.ingestion.ast_parser import parse_repository

    fixtures = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"
    parse_result = parse_repository(fixtures)
    chunks = ContextEngine.chunks_from_parse_result(parse_result)

    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.file_path != "", f"Chunk {chunk.id} has no file_path"
        assert chunk.line_start >= 0
