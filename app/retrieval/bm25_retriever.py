import re
from functools import lru_cache
from rank_bm25 import BM25Okapi
from app.vectorstore.chroma import get_collection

STOPWORDS = {
    "zx", "bank", "ltd", "provided", "key", "features", "types", 
    "what", "are", "the", "of", "for", "in", "a", "an", "by", "is", "to"
}

def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    filtered = [t for t in tokens if t not in STOPWORDS]
    # Fallback to standard tokens if everything got filtered out
    return filtered if filtered else tokens

@lru_cache(maxsize=1)
def _load_index():
    data = get_collection().get(include=["documents", "metadatas"])
    tokenized = [_tokenize(doc) for doc in data["documents"]]
    bm25 = BM25Okapi(tokenized)
    return bm25, data["ids"], data["documents"], data["metadatas"]

def retrieve_bm25(query: str, top_k: int = 50) -> list[dict]:
    bm25, ids, documents, metadatas = _load_index()
    scores = bm25.get_scores(_tokenize(query))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {"chunk_id": ids[i], "text": documents[i], "metadata": metadatas[i], "score": scores[i]}
        for i in ranked
    ]