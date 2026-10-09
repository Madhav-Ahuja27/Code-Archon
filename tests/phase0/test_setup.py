"""Phase 0 — Skeleton & Tooling Setup tests.

Gate: all 5 pass before Phase 1 begins.
"""

from __future__ import annotations

import os
import pytest


# ── Test 1: all archon.* modules import cleanly ─────────────────────────────

def test_imports_all_modules():
    """Every archon submodule must be importable without error."""
    import archon
    import archon.config
    import archon.agent.loop
    import archon.agent.harness
    import archon.ingestion.ast_parser
    import archon.ingestion.git_reader
    import archon.graph.neo4j_client
    import archon.graph.network_graph
    import archon.retrieval.bm25
    import archon.retrieval.vector_store
    import archon.tools.static
    import archon.tools.runtime
    import archon.tools.search
    import archon.tools.git_tools
    import archon.verification.harness
    import archon.verification.hallucination
    import archon.memory.sqlite_store
    import archon.memory.redis_store
    import archon.docs.generator
    import archon.goal_analyzer
    assert archon.__version__ == "0.1.0"


# ── Test 2: .env parsed, required keys present ───────────────────────────────

def test_env_loads():
    """Config must expose all required keys from .env."""
    from archon.config import cfg
    assert cfg.neo4j_uri.startswith("bolt://"), f"bad neo4j_uri: {cfg.neo4j_uri}"
    assert cfg.neo4j_user, "neo4j_user empty"
    assert cfg.neo4j_password, "neo4j_password empty"
    assert cfg.redis_url.startswith("redis://"), f"bad redis_url: {cfg.redis_url}"
    assert cfg.llm_model, "llm_model empty"
    assert cfg.max_agent_iterations > 0
    assert cfg.max_context_tokens > 0
    assert cfg.tool_call_limit_per_iter > 0


# ── Test 3: Neo4j bolt connection ────────────────────────────────────────────

def test_neo4j_reachable():
    """Neo4j bolt must be reachable and authenticate successfully."""
    from archon.config import cfg
    from neo4j import GraphDatabase, exceptions as neo4j_exc

    try:
        driver = GraphDatabase.driver(
            cfg.neo4j_uri,
            auth=(cfg.neo4j_user, cfg.neo4j_password),
        )
        driver.verify_connectivity()
        driver.close()
    except neo4j_exc.ServiceUnavailable:
        pytest.skip("Neo4j not running — start with: docker-compose up -d neo4j")
    except neo4j_exc.AuthError as e:
        pytest.fail(f"Neo4j auth failed: {e}")


# ── Test 4: Redis ping ───────────────────────────────────────────────────────

def test_redis_reachable():
    """Redis must respond to PING."""
    from archon.config import cfg
    import redis as redis_lib

    try:
        r = redis_lib.from_url(cfg.redis_url, socket_connect_timeout=3)
        assert r.ping(), "Redis did not respond to PING"
    except redis_lib.ConnectionError:
        pytest.skip("Redis not running — start with: docker-compose up -d redis")


# ── Test 5: ChromaDB client initialises and creates a collection ─────────────

def test_chroma_init(tmp_path):
    """ChromaDB must initialise and create a named collection without error."""
    import chromadb

    client = chromadb.PersistentClient(path=str(tmp_path / "chroma_test"))
    col = client.get_or_create_collection("phase0_test")
    assert col is not None
    assert col.name == "phase0_test"
    # clean up
    client.delete_collection("phase0_test")
