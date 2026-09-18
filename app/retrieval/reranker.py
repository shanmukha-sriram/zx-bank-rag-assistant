import os
from functools import lru_cache
from sentence_transformers import CrossEncoder

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@lru_cache(maxsize=1)
def _get_model() -> CrossEncoder:
    return CrossEncoder(os.getenv("RERANKER_MODEL", DEFAULT_MODEL))


def rerank(query: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
    if not chunks:
        return []

    scores = _get_model().predict([(query, c["text"]) for c in chunks])
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    return sorted(chunks, key=lambda c: c["rerank_score"], reverse=True)[:top_k]