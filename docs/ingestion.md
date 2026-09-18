# Ingestion Pipeline

## Overview
Ingestion turns raw `.md` files into clean, structured `Section` objects that chunking can safely split. Three small, independently testable stages: load → clean → parse.

## Loading — `app/ingestion/loader.py`
Finds every `.md` file under `data/raw/zx_bank/` and reads it into a `RawDocument` (source filename, a slugified `document_id`, raw text). Deliberately does no interpretation of content — a loader's only job is finding and reading bytes.

## Cleaning — `app/ingestion/cleaner.py`
Normalizes whitespace before parsing:
- Converts `\r\n` to `\n`
- Strips trailing whitespace on lines
- Collapses 3+ blank lines to a single blank line

This runs before parsing so heading detection and section splitting aren't thrown off by inconsistent formatting from different document authors.

## Parsing — `app/ingestion/parser.py`
Splits cleaned text into `Section` objects using Markdown heading levels (`#` through `######`), preserving:
- `heading` — the section's own heading text
- `level` — heading depth (1–6)
- `heading_path` — full ancestry, e.g. `House Loan > Eligibility`
- `content` — the section's body text

`heading_path` is the single most important field in the whole pipeline — it's what makes citations traceable back to a real location in a real document, rather than just "somewhere in this file."

## Metadata Design
Every chunk (see `docs/chunking.md`) carries:
```json
{
  "document_id": "zx-house-loan",
  "source": "ZX Bank House Loan.md",
  "section": "Eligibility",
  "heading_path": "House Loan > Eligibility",
  "chunk_id": "zx-house-loan-eligibility-00"
}
```
This metadata is generated once, at ingestion time, and carried unchanged through embedding, storage, retrieval, and into the final citation — never reconstructed or guessed later in the pipeline.

## Indexing
`scripts/ingest.py` runs the full chain: load → clean → parse → chunk → embed → store in ChromaDB. It's the single re-indexing entry point — run it whenever source documents, chunking strategy, or the embedding model changes.
