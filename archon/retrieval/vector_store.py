"""Vector store: ChromaDB when it works, a built-in in-memory index when it does not.

ChromaDB ships a native (Rust) engine. On some machines (e.g. Windows without the
Microsoft Visual C++ runtime) it fails to load with "DLL load failed". Rather than
crash the whole tool, VectorStore then falls back to a small pure-Python cosine
index over the same embeddings, so retrieval, the agent and the CLI keep working.

Embeddings: with use_hash_embed=True, text is embedded by feature hashing of its
words (cosine similarity ~ shared vocabulary; deterministic, offline, no download).
Otherwise ChromaDB's default model (MiniLM) is attempted.
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
import uuid
from pathlib import Path
from typing import Optional

from archon.retrieval.bm25 import Chunk

log = logging.getLogger(__name__)

_DIM = 256


def _lexical_embed(text: str, dim: int = _DIM) -> list[float]:
    """Feature-hashing bag-of-words embedding, L2-normalised."""
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(text))        # camelCase -> words
    vec = [0.0] * dim
    for tok in re.findall(r"[a-z0-9]+", text.lower().replace("_", " ")):
        h = hashlib.md5(tok.encode()).digest()
        vec[int.from_bytes(h[:4], "little") % dim] += 1.0 if h[4] & 1 else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def _make_chroma_hash_ef():
    """Chroma EmbeddingFunction wrapping _lexical_embed (built lazily: needs chromadb)."""
    from chromadb import Documents, EmbeddingFunction, Embeddings

    class _LexicalEmbeddingFunction(EmbeddingFunction):
        def __init__(self):
            pass

        def __call__(self, input: Documents) -> Embeddings:  # noqa: A002
            return [_lexical_embed(t) for t in input]

        def name(self) -> str:
            return "lexical_hash_embedding"

    return _LexicalEmbeddingFunction()


def _default_ef():
    """Chroma's default model EF; lexical hashing if unavailable."""
    try:
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
        return DefaultEmbeddingFunction()
    except Exception:
        return _make_chroma_hash_ef()


# ── Vector Store ──────────────────────────────────────────────────────────────

class VectorStore:
    """Semantic chunk retrieval. Each instance is isolated (unique collection).

    `self.backend` is "chromadb" or "builtin" so callers can report which is in use.
    """

    def __init__(
        self,
        persist_path: Optional[str | Path] = None,
        use_hash_embed: bool = False,
        collection_name: Optional[str] = None,
    ):
        self._collection_name = collection_name or f"archon_{uuid.uuid4().hex}"
        self._fallback: Optional[dict[str, tuple[Chunk, list[float]]]] = None
        self._client = None
        self._col = None
        self.backend = "chromadb"
        try:
            import chromadb
            if persist_path:
                self._client = chromadb.PersistentClient(path=str(persist_path))
            else:
                self._client = chromadb.EphemeralClient()
            ef = _make_chroma_hash_ef() if use_hash_embed else _default_ef()
            self._col = self._client.get_or_create_collection(
                self._collection_name, embedding_function=ef
            )
        except Exception as e:      # ImportError, "DLL load failed", sqlite problems...
            log.warning("ChromaDB unavailable (%s) - using built-in in-memory vector index", e)
            self._fallback = {}
            self._client = self._col = None
            self.backend = "builtin"

    def add_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        if self._fallback is not None:
            for c in chunks:
                self._fallback[c.id] = (c, _lexical_embed(c.text))
            return
        for i in range(0, len(chunks), 500):
            batch = chunks[i:i + 500]
            self._col.upsert(
                ids=[c.id for c in batch],
                documents=[c.text for c in batch],
                metadatas=[{
                    "file_path": c.file_path,
                    "line_start": c.line_start,
                    "line_end": c.line_end,
                } for c in batch],
            )

    def query(self, query: str, top_k: int = 10) -> list[Chunk]:
        if self._fallback is not None:
            if not self._fallback:
                return []
            q = _lexical_embed(query)
            scored = []
            for chunk, vec in self._fallback.values():
                cos = sum(a * b for a, b in zip(q, vec))
                scored.append(((cos + 1.0) / 2.0, chunk))
            scored.sort(key=lambda t: t[0], reverse=True)
            return [Chunk(id=c.id, text=c.text, file_path=c.file_path,
                          line_start=c.line_start, line_end=c.line_end, score=sc)
                    for sc, c in scored[:top_k]]

        count = self._col.count()
        if count == 0:
            return []
        results = self._col.query(query_texts=[query], n_results=min(top_k, count))
        chunks = []
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i] if results.get("distances") else 0.0
            chunks.append(Chunk(
                id=doc_id,
                text=results["documents"][0][i],
                file_path=meta.get("file_path", ""),
                line_start=int(meta.get("line_start", 0)),
                line_end=int(meta.get("line_end", 0)),
                score=1.0 / (1.0 + dist),
            ))
        return chunks

    def count(self) -> int:
        return len(self._fallback) if self._fallback is not None else self._col.count()

    def clear(self) -> None:
        if self._fallback is not None:
            self._fallback.clear()
            return
        self._client.delete_collection(self._collection_name)
        self._col = self._client.get_or_create_collection(self._collection_name)


# ── Context Engine ────────────────────────────────────────────────────────────

class ContextEngine:
    """Hybrid BM25 + vector retrieval with token-budget context assembly."""

    def __init__(self, bm25_index, vector_store: VectorStore,
                 max_tokens: int = 6000):
        self._bm25 = bm25_index
        self._vs = vector_store
        self._max_tokens = max_tokens

    def query(self, goal: str, top_k: int = 10) -> list[Chunk]:
        bm25_results = self._bm25.query(goal, top_k=top_k)
        vec_results = self._vs.query(goal, top_k=top_k)
        seen: dict[str, Chunk] = {}
        for chunk in bm25_results + vec_results:
            if chunk.id not in seen or chunk.score > seen[chunk.id].score:
                seen[chunk.id] = chunk
        return sorted(seen.values(), key=lambda c: c.score, reverse=True)

    def build_context_window(self, chunks: list[Chunk]) -> str:
        char_budget = self._max_tokens * 4
        parts: list[str] = []
        used = 0
        for chunk in chunks:
            header = f"# {chunk.id} [{chunk.file_path}:{chunk.line_start}]\n"
            block = header + chunk.text + "\n\n"
            if used + len(block) > char_budget:
                break
            parts.append(block)
            used += len(block)
        return "".join(parts)

    @staticmethod
    def chunks_from_parse_result(parse_result) -> list[Chunk]:
        chunks: list[Chunk] = []
        for fn in parse_result.functions:
            text_parts = []
            if fn.docstring:
                text_parts.append(fn.docstring)
            text_parts.append(f"def {fn.name}({', '.join(fn.args)})")
            if fn.calls:
                text_parts.append(f"calls: {', '.join(fn.calls)}")
            chunks.append(Chunk(
                id=fn.id,
                text="\n".join(text_parts),
                file_path=fn.module_path,
                line_start=fn.line_start,
                line_end=fn.line_end,
            ))
        for cls in parse_result.classes:
            text_parts = [f"class {cls.name}"]
            if cls.bases:
                text_parts.append(f"bases: {', '.join(cls.bases)}")
            if cls.docstring:
                text_parts.append(cls.docstring)
            chunks.append(Chunk(
                id=cls.id,
                text="\n".join(text_parts),
                file_path=cls.module_path,
                line_start=cls.line_start,
                line_end=cls.line_end,
            ))
        return chunks
