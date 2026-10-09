import types
import pytest
from archon import llm
from archon.agent.loop import parse_verdict


def _fake_groq(model_ids):
    class _Models:
        def list(self):
            return types.SimpleNamespace(data=[types.SimpleNamespace(id=i) for i in model_ids])
    class _Groq:
        def __init__(self, api_key): self.models = _Models()
    return _Groq


@pytest.fixture(autouse=True)
def _clear_cache():
    llm._groq_model_cache.clear()


def test_keeps_wanted_when_available(monkeypatch):
    import groq
    monkeypatch.setattr(groq, "Groq", _fake_groq(["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]))
    assert llm._pick_groq_model("k_abcdef", "llama-3.3-70b-versatile") == "llama-3.3-70b-versatile"


def test_falls_back_when_wanted_missing(monkeypatch):
    import groq
    monkeypatch.setattr(groq, "Groq", _fake_groq(["openai/gpt-oss-20b", "openai/gpt-oss-120b", "whisper-large-v3"]))
    assert llm._pick_groq_model("k_abcdef", "llama-3.3-70b-versatile") == "openai/gpt-oss-120b"


def test_ignores_non_chat_models(monkeypatch):
    import groq
    monkeypatch.setattr(groq, "Groq", _fake_groq(["whisper-large-v3", "playai-tts"]))
    assert llm._pick_groq_model("k_abcdef", "llama-3.3-70b-versatile") == "llama-3.3-70b-versatile"


def test_list_failure_keeps_wanted(monkeypatch):
    import groq
    class _Boom:
        def __init__(self, api_key): raise ConnectionError("blocked")
    monkeypatch.setattr(groq, "Groq", _Boom)
    assert llm._pick_groq_model("k_abcdef", "openai/gpt-oss-120b") == "openai/gpt-oss-120b"


@pytest.mark.parametrize("text,expected", [
    ("VERIFIED", "VERIFIED"), ("verified.", "VERIFIED"),
    ("UNVERIFIED", "UNCERTAIN"), ("not verified", "UNCERTAIN"),
    ("REFUTED", "REFUTED"), ("UNCERTAIN", "UNCERTAIN"),
    ("", "UNCERTAIN"), ("maybe?", "UNCERTAIN"),
])
def test_parse_verdict(text, expected):
    assert parse_verdict(text) == expected
