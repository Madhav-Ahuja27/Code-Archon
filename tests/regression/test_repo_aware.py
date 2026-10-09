"""Repo-aware goal decomposition, failure reasons, search-term retries, --task flag."""

import logging
import re
from pathlib import Path

import pytest

from archon.agent.harness import Harness, HarnessConfig
from archon.agent.loop import (AgentState, Evidence, Hypothesis, _evidence_for_claim,
                               build_agent_graph)
from archon.goal_analyzer import GoalAnalyzer
from archon.graph.builder import build_graph
from archon.graph.neo4j_client import make_graph_store
from archon.ingestion.ast_parser import parse_repository
from archon.repo_summary import summarize_repo
from archon.retrieval.bm25 import BM25Index
from archon.retrieval.vector_store import ContextEngine, VectorStore

FIX = Path(__file__).parent.parent.parent / "fixtures" / "sample_repo"


class _Resp:
    def __init__(self, c): self.content = c


# ── repo summary ────────────────────────────────────────────────────────────

def test_repo_summary_describes_python_repo():
    s = summarize_repo(parse_repository(FIX))
    assert "Language: Python" in s
    assert "auth.py" in s and "UserAuth" in s
    assert "flask" in s            # declared dependency from requirements.txt


def test_repo_summary_excludes_tests(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_big.py").write_text("x = 1\n" * 500, encoding="utf-8")
    (tmp_path / "lib.py").write_text("def f():\n    pass\n", encoding="utf-8")
    s = summarize_repo(parse_repository(tmp_path))
    assert "lib.py" in s and "tests/test_big.py" not in s


# ── goal analyzer gets repo context ─────────────────────────────────────────

class _CaptureLLM:
    def __init__(self): self.messages = None
    def invoke(self, messages):
        self.messages = messages
        return _Resp('{"objective":"o","focus_modules":[],"investigation_tasks":["t1","t2"],'
                     '"success_criteria":["c"]}')


def test_goal_analyzer_sends_repo_summary_and_python_constraint():
    llm = _CaptureLLM()
    g = GoalAnalyzer(llm=llm).analyze("understand routing", repo_summary="MARKER_123 Flask app.py")
    assert g.investigation_tasks == ["t1", "t2"]
    system, human = str(llm.messages[0].content), str(llm.messages[-1].content)
    assert "MARKER_123" in human and "Repository" in human
    assert "Python" in system and "other languages" in system


def test_goal_analyzer_without_summary_has_no_repository_section():
    llm = _CaptureLLM()
    GoalAnalyzer(llm=llm).analyze("understand routing")
    assert "Repository:" not in str(llm.messages[-1].content)


# ── cited-evidence verification ─────────────────────────────────────────────

def _state(claim):
    return AgentState(hypothesis=Hypothesis(claim=claim), evidence=[
        Evidence(source="a.py:1", content="x"), Evidence(source="b.py:2", content="y"),
        Evidence(source="c.py:3", content="z")])


def test_verifier_sees_only_cited_evidence():
    got = _evidence_for_claim(_state("It lives in b.py:2."))
    assert [e.source for e in got] == ["b.py:2"]


def test_verifier_sees_all_evidence_when_nothing_cited():
    assert len(_evidence_for_claim(_state("no citation"))) == 3


def test_verifier_falls_back_to_all_when_citation_matches_nothing():
    assert len(_evidence_for_claim(_state("see z.py:9"))) == 3


# ── retries: failure reasons + LLM search terms ─────────────────────────────

def _setup():
    pr = parse_repository(FIX)
    store = make_graph_store(force_inmemory=True); build_graph(pr, store)
    chunks = ContextEngine.chunks_from_parse_result(pr)
    bm25 = BM25Index(); bm25.build(chunks)
    vs = VectorStore(use_hash_embed=True); vs.add_chunks(chunks)
    return store, ContextEngine(bm25, vs), pr


class TermsLLM:
    """Says INSUFFICIENT until the evidence contains hash_password; suggests that term on retry."""
    def __init__(self): self.terms_prompt = None
    def invoke(self, messages):
        system, human = str(messages[0].content), str(messages[-1].content)
        if "search a Python codebase" in system:
            self.terms_prompt = human
            return _Resp("hash_password, verify_password")
        if "code archaeologist" in system:
            m = re.search(r"\[([\w/.\\-]+\.py:\d+)\] \(ripgrep\) def hash_password", human)
            return _Resp(f"Hashing is in {m.group(1)}." if m else "INSUFFICIENT")
        return _Resp("VERIFIED")


def test_suggested_search_terms_rescue_a_failed_task(caplog):
    store, engine, pr = _setup()
    llm = TermsLLM()
    h = Harness(HarnessConfig(allowed_tools={"ripgrep"}, call_limit_per_tool=5))
    g = build_agent_graph(llm=llm, harness=h, store=store, max_iterations=6,
                          ctx_engine=engine, repo_root=FIX, repo_summary="REPO_SUMMARY_MARK")
    with caplog.at_level(logging.INFO, logger="archon.agent.loop"):
        final = g.invoke(AgentState(goal="g", tasks=["zebra quantum"]).model_dump())
    assert len(final["findings"]) == 1 and final["unknowns"] == []
    assert "REPO_SUMMARY_MARK" in llm.terms_prompt            # retry prompt is repo-aware
    assert "insufficient" in llm.terms_prompt                 # ... and knows why it failed
    assert "previous attempt failed: model judged" in caplog.text
    assert "new search terms: hash_password" in caplog.text


class FabLLM:
    def invoke(self, messages):
        if "code archaeologist" in str(messages[0].content):
            return _Resp("It is in ghost/x.py:1.")
        if "search a Python codebase" in str(messages[0].content):
            return _Resp("")
        return _Resp("VERIFIED")


def test_gate_block_reason_is_logged(caplog):
    store, engine, _ = _setup()
    h = Harness(HarnessConfig(allowed_tools={"ripgrep"}, call_limit_per_tool=5))
    g = build_agent_graph(llm=FabLLM(), harness=h, store=store, max_iterations=6,
                          ctx_engine=engine, repo_root=FIX)
    with caplog.at_level(logging.INFO, logger="archon.agent.loop"):
        final = g.invoke(AgentState(goal="g", tasks=["authentication password"]).model_dump())
    assert final["findings"] == [] and len(final["rejected"]) >= 1
    assert "previous attempt failed: provenance gate" in caplog.text
    assert "giving up on task 1/1 (provenance gate" in caplog.text


# ── CLI --task (deterministic demo, no LLM decomposition) ───────────────────

def test_cli_task_flag_skips_decomposition(tmp_path, monkeypatch):
    from typer.testing import CliRunner
    from archon import cli
    from archon.graph import neo4j_client as nc
    monkeypatch.setattr(nc, "make_graph_store", lambda **k: nc._InMemoryStore())
    r = CliRunner().invoke(cli.app, [
        "investigate", str(FIX), "--goal", "x", "--output", str(tmp_path / "out"),
        "--no-llm", "--task", "authentication password hashing", "--task", "login flow"])
    assert r.exit_code == 0, r.output
    report = (tmp_path / "out" / "report.md").read_text(encoding="utf-8")
    assert "authentication password hashing" in report and "login flow" in report


# ── prompt evidence is balanced across tools ────────────────────────────────

def test_prompt_evidence_is_balanced_across_tools():
    from archon.agent.loop import _balanced
    ev = ([Evidence(source=f"r{i}.py:1", content="c", tool="retrieval") for i in range(30)]
          + [Evidence(source=f"g{i}.py:1", content="c", tool="ripgrep") for i in range(5)]
          + [Evidence(source=f"x{i}.py:1", content="c", tool="graph") for i in range(3)])
    picked = _balanced(ev, 14)
    tools = [e.tool for e in picked]
    assert len(picked) == 14
    assert tools.count("ripgrep") == 5 and tools.count("graph") == 3   # none crowded out
    assert tools.count("retrieval") == 6


def test_balanced_handles_small_and_empty_inputs():
    from archon.agent.loop import _balanced
    assert _balanced([], 14) == []
    one = [Evidence(source="a.py:1", content="c", tool="x")]
    assert _balanced(one, 14) == one
