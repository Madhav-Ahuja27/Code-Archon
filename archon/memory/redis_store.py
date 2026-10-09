"""Redis cross-session memory — stores repo investigation summaries."""

from __future__ import annotations

import json
import logging
from typing import Optional

log = logging.getLogger(__name__)

_TTL_SECONDS = 60 * 60 * 24 * 30   # 30 days


def _key(repo_hash: str) -> str:
    return f"archon:repo:{repo_hash}:summary"


class RedisStore:
    """Cross-session persistent memory backed by Redis."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        import redis
        self._r = redis.from_url(redis_url, decode_responses=True,
                                 socket_connect_timeout=3)

    def ping(self) -> bool:
        try:
            return self._r.ping()
        except Exception:
            return False

    def save_repo_summary(self, repo_hash: str, summary: dict) -> None:
        key = _key(repo_hash)
        self._r.set(key, json.dumps(summary), ex=_TTL_SECONDS)

    def load_repo_summary(self, repo_hash: str) -> Optional[dict]:
        key = _key(repo_hash)
        raw = self._r.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def ttl(self, repo_hash: str) -> int:
        """Return TTL in seconds, -1 if key missing."""
        return self._r.ttl(_key(repo_hash))

    def delete(self, repo_hash: str) -> None:
        self._r.delete(_key(repo_hash))


class _MockRedisStore:
    """In-memory Redis mock for tests without a Redis instance."""

    def __init__(self):
        self._store: dict[str, str] = {}
        self._ttls: dict[str, int] = {}

    def ping(self) -> bool:
        return True

    def save_repo_summary(self, repo_hash: str, summary: dict) -> None:
        self._store[_key(repo_hash)] = json.dumps(summary)
        self._ttls[_key(repo_hash)] = _TTL_SECONDS

    def load_repo_summary(self, repo_hash: str) -> Optional[dict]:
        raw = self._store.get(_key(repo_hash))
        return json.loads(raw) if raw is not None else None

    def ttl(self, repo_hash: str) -> int:
        return self._ttls.get(_key(repo_hash), -1)

    def delete(self, repo_hash: str) -> None:
        self._store.pop(_key(repo_hash), None)
        self._ttls.pop(_key(repo_hash), None)


def make_redis_store(redis_url: str = "redis://localhost:6379"):
    """Return a real RedisStore if available, else an in-memory mock."""
    try:
        store = RedisStore(redis_url)
        if store.ping():
            return store
    except Exception as e:
        log.info("Redis unavailable (%s), using in-memory mock", e)
    return _MockRedisStore()
