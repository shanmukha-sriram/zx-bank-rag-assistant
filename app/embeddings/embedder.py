import os
from functools import lru_cache
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL))


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    return model.encode(texts, show_progress_bar=False, normalize_embeddings=True).tolist()