"""LLM factory — returns a LangChain BaseChatModel from config."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


# Best-first. Used only when the configured model is not available to this key.
_GROQ_PREFERENCE = [
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "llama-3.1-8b-instant",
]
_groq_model_cache: dict[tuple[str, str], str] = {}


def _pick_groq_model(api_key: str, wanted: str) -> str:
    """Ask Groq which models this key can use; keep `wanted` if available,
    otherwise fall back to the best available chat model from the preference list."""
    key = (api_key[-6:], wanted)
    if key in _groq_model_cache:
        return _groq_model_cache[key]
    chosen = wanted
    try:
        from groq import Groq
        available = {m.id for m in Groq(api_key=api_key).models.list().data}
        if wanted in available:
            chosen = wanted
        else:
            chosen = next((m for m in _GROQ_PREFERENCE if m in available), wanted)
            if chosen != wanted:
                log.warning("Groq model %r not available to this key; using %r",
                            wanted, chosen)
    except Exception as e:   # offline / list endpoint blocked: just try `wanted`
        log.info("Could not list Groq models (%s); using %r", e, wanted)
    _groq_model_cache[key] = chosen
    return chosen


def make_llm(provider: str | None = None, model: str | None = None):
    """Return a LangChain chat model.

    Priority: provider arg > GROQ_API_KEY > ANTHROPIC_API_KEY > raises.
    """
    from archon.config import cfg

    p = (provider or cfg.llm_provider).lower()
    m = model or cfg.llm_model

    if p == "groq" or (not p and cfg.groq_api_key):
        from langchain_groq import ChatGroq
        m = _pick_groq_model(cfg.groq_api_key, m)
        log.info("Using Groq — model: %s", m)
        return ChatGroq(
            model=m,
            api_key=cfg.groq_api_key,
            temperature=0.0,
            max_tokens=4096,
            max_retries=6,      # free tier rate-limits (429); retry with backoff
        )

    if p == "anthropic" or (not p and cfg.anthropic_api_key):
        from langchain_anthropic import ChatAnthropic
        log.info("Using Anthropic — model: %s", m)
        return ChatAnthropic(
            model=m,
            api_key=cfg.anthropic_api_key,
            temperature=0.0,
            max_tokens=4096,
        )

    if p == "openai" or (not p and cfg.openai_api_key):
        from langchain_openai import ChatOpenAI
        log.info("Using OpenAI — model: %s", m)
        return ChatOpenAI(
            model=m,
            api_key=cfg.openai_api_key,
            temperature=0.0,
            max_tokens=4096,
        )

    raise ValueError(
        f"No valid LLM provider configured. "
        f"Set GROQ_API_KEY / ANTHROPIC_API_KEY / OPENAI_API_KEY in .env"
    )
