"""BM25 retriever over source code chunks."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from rank_bm25 import BM25Okapi

log = logging.getLogger(__name__)


@dataclass
class Chunk:
    """A retrievable unit of source code."""
    id: str                  # unique: "file.py::ClassName::fn_name"
    text: str                # docstring + body text
    file_path: str
    line_start: int = 0
    line_end: int = 0
    score: float = 0.0       # filled in during retrieval


class BM25Index:
    """Keyword index over a corpus of Chunks."""

    def __init__(self):
        self._chunks: list[Chunk] = []
        self._index: BM25Okapi | None = None

    def build(self, chunks: list[Chunk]) -> None:
        self._chunks = list(chunks)
        tokenized = [c.text.lower().split() for c in self._chunks]
        self._index = BM25Okapi(tokenized) if tokenized else None
        log.debug("BM25 index built with %d chunks", len(self._chunks))

    def query(self, query: str, top_k: int = 10) -> list[Chunk]:
        if not self._index or not self._chunks:
            return []
        tokens = query.lower().split()
        scores = self._index.get_scores(tokens)
        ranked = sorted(
            zip(scores, self._chunks), key=lambda x: x[0], reverse=True
        )
        results = []
        for score, chunk in ranked[:top_k]:
            c = Chunk(**chunk.__dict__)
            c.score = float(score)
            results.append(c)
        return results

    def size(self) -> int:
        return len(self._chunks)
