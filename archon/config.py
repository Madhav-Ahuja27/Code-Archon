"""Central configuration — reads from environment / .env file."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    # LLM
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    llm_provider: str = os.getenv("LLM_PROVIDER", "groq")
    llm_model: str = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

    # Neo4j
    neo4j_uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("NEO4J_PASSWORD", "archon-dev")

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # ChromaDB
    chroma_path: Path = Path(os.getenv("CHROMA_PATH", "./data/chroma"))

    # Agent tuning
    max_agent_iterations: int = int(os.getenv("MAX_AGENT_ITERATIONS", "20"))
    max_context_tokens: int = int(os.getenv("MAX_CONTEXT_TOKENS", "6000"))
    tool_call_limit_per_iter: int = int(os.getenv("TOOL_CALL_LIMIT_PER_ITER", "5"))

    # Paths
    project_root: Path = Path(__file__).parent.parent
    output_dir: Path = project_root / "output"
    data_dir: Path = project_root / "data"


cfg = Config()
