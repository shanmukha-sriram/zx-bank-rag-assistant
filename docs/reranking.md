# Reranking

## Why Rerank At All
Vector and BM25 retrieval are candidate generators — fast, but they score query and document independently (a bi-encoder architecture), so they can't capture fine-grained relevance between a specific query and a specific chunk. A cross-encoder reads the query and the chunk *together* in one pass, producing a much more accurate relevance score at the cost of being too slow to run over an entire corpus.

## Implementation — `app/retrieval/reranker.py`
`cross-encoder/ms-marco-MiniLM-L-6-v2` (configurable via `RERANKER_MODEL`) scores each of the ~20 hybrid-retrieved candidates against the query, and only the top 5 by that score reach the LLM.

## Latency vs. Quality
Reranking adds real, measurable latency (a forward pass per candidate) in exchange for higher-precision context. This is exactly the kind of tradeoff `docs/experiments.md` is meant to make visible with numbers rather than leave as a vague assumption.

## Abstention Depends On This Score
The reranker's top score also feeds `app/generation/abstention.py` — if the best candidate still scores below threshold, the system abstains before ever calling the LLM. This makes reranking load-bearing for safety, not just answer quality.
