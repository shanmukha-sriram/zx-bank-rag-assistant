# Chunking Strategy

## Approach: Structure-Aware Chunking
Rather than splitting documents by a fixed character/token window blind to content, chunking operates on the `Section` objects produced by the parser — so a chunk boundary never falls in the middle of an unrelated topic. A short section (e.g. "Eligibility") becomes exactly one chunk; a long section is split further with overlap.

## Parameters
- `CHUNK_SIZE=600` (words) — approximates the target 500–800 *token* range from the original spec (~600 words ≈ 780 tokens at ~1.3 tokens/word for English).
- `CHUNK_OVERLAP=100` (words) — ensures a sentence or idea split across a boundary still has context on both sides.

Both are environment-configurable (`app/ingestion/chunker.py` reads them via `.env`), not hardcoded — re-tunable without a code change.

## Why word counts instead of a real tokenizer
Word count is used as a deliberate approximation rather than pulling in a tokenizer library just for chunk sizing. This is a documented simplification (see `docs/decisions.md`) — accurate enough for this corpus size, and avoids adding a dependency whose only job would be sizing.

## Chunk ID Scheme
`{document_id}-{slugified-heading}-{index}`, e.g. `zx-house-loan-eligibility-00`. Human-readable, traceable back to its source section, and stable across re-indexing runs as long as heading text doesn't change.

## Tuning
Chunk size/overlap should be set from real corpus statistics (`docs/data.md` — average/min/max document length), not guessed, and re-validated against retrieval metrics (`docs/evaluation.md`) rather than assumed correct.
