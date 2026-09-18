# Retrieval Architecture

## Why Hybrid Retrieval
Vector search alone is strong for semantic/paraphrased questions ("what's needed to qualify for a loan") but can miss exact terms — product codes, specific rates, exact policy names — because embeddings compress specifics into meaning. BM25 is the reverse: strong on exact keyword/term matches, weak on paraphrase. Running both and combining catches what either one alone would miss.

## Vector Search — `app/retrieval/vector_retriever.py`
Embeds the query with the same model used to embed chunks (`sentence-transformers/all-MiniLM-L6-v2` by default, swappable via `EMBEDDING_MODEL`), then queries ChromaDB for nearest neighbors by cosine similarity.

## BM25 — `app/retrieval/bm25_retriever.py`
Classic term-frequency keyword search (`rank-bm25`), built directly from the same chunk text stored in ChromaDB — one source of truth, no separate index to keep in sync.

## Combining: Reciprocal Rank Fusion — `app/retrieval/fusion.py`
```
score(chunk) = sum(1 / (k + rank_in_list)) across all rankers
```
RRF was chosen over a weighted-score blend because vector similarity and BM25 scores live on completely different, incomparable scales — RRF sidesteps that by fusing on *rank position* instead of raw score. `k=60` is the standard constant from the original RRF paper; it damps how much any single ranker's #1 pick can dominate the fused order.

## Parameters
- Candidate generation: `top_k=20` from each of vector and BM25 (wide net, high recall)
- After reranking (`docs/reranking.md`): `top_k=5` reaches the LLM (narrow, high precision)
- Both configurable via `.env` (`TOP_K`)
