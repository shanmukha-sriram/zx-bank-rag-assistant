# ZX Bank AI Knowledge Assistant

A production-oriented Retrieval-Augmented Generation (RAG) system that answers natural-language questions about ZX Bank's internal knowledge documents with grounded, citation-backed answers — and refuses to answer when it doesn't have the evidence.

## Overview

Users can ask plain-English questions about ZX Bank's products and policies instead of manually searching through dozens of Markdown documents. Every answer is traceable back to a specific document and section; questions the corpus can't support are refused rather than guessed at.

## Problem Statement

Internal knowledge is scattered across many long Markdown documents. Finding a specific answer (an eligibility rule, a rate, a required document) means manually searching multiple files, and there's no way to know whether an answer is actually grounded in the source material.

## Solution

A hybrid-retrieval RAG pipeline: documents are chunked with their heading structure preserved, indexed for both semantic (vector) and keyword (BM25) search, fused and reranked for relevance, then passed to an LLM that must cite its sources — with an explicit, score-based refusal path when evidence is insufficient.

## Key Features

- Structure-aware Markdown chunking that preserves heading hierarchy
- Hybrid retrieval: vector search + BM25 combined via Reciprocal Rank Fusion
- Cross-encoder reranking for precision
- Citation-enforced, grounded generation with citation validation
- Score-based abstention (not just an LLM self-report)
- Golden-dataset evaluation: Recall@K, Precision@K, MRR, Faithfulness, Answer Relevance, Abstention Accuracy
- FastAPI backend + Streamlit chat UI
- Automated tests, Docker packaging, and a CI/CD pipeline with a quality gate

## Architecture

```
User → Streamlit UI → FastAPI → RAG Pipeline
                                     │
                         ┌───────────┴───────────┐
                         ▼                        ▼
                  Vector Search               BM25 Search
                         └───────────┬───────────┘
                                     ▼
                        Reciprocal Rank Fusion
                                     ▼
                          Cross-Encoder Reranker
                                     ▼
                     Abstention Check (score gate)
                            ↙            ↘
                    Abstain Message      LLM Generation
                                              ▼
                                   Citation Validation
                                              ▼
                                       Final Answer
```

Indexing pipeline: `Markdown → Loader → Cleaner → Parser → Chunker → Embedder → ChromaDB`

## Tech Stack

| Layer | Choice |
|---|---|
| Core | Python, FastAPI, Pydantic |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector store | ChromaDB |
| Keyword search | rank-bm25 |
| Reranking | sentence-transformers CrossEncoder (`ms-marco-MiniLM-L-6-v2`) |
| LLM | Groq (`openai/gpt-oss-120b`, swappable) |
| Evaluation | Custom retrieval + LLM-as-judge generation metrics |
| Frontend | Streamlit |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Quality | pytest, ruff |

See `docs/decisions.md` for why each of these was chosen over the alternatives.

## RAG Pipeline

1. Query goes to hybrid retrieval (vector + BM25 candidates, top 20 each)
2. Results fused with Reciprocal Rank Fusion
3. Fused candidates reranked by a cross-encoder, top 5 kept
4. If the top rerank score is below threshold → abstain, no LLM call
5. Otherwise, top chunks + query go to the LLM with a citation-enforcing system prompt
6. Answer is checked for citation validity before being returned

## Dataset

ZX Bank Markdown corpus (RAG-Multi-Corpus dataset). See `docs/data.md` for corpus statistics, categories, and known limitations.

## Project Structure

```
zx-bank-rag/
├── app/
│   ├── main.py
│   ├── api/{routes,schemas}/
│   ├── core/{logging.py,exceptions.py}
│   ├── ingestion/{loader,cleaner,parser,chunker}.py
│   ├── embeddings/embedder.py
│   ├── vectorstore/chroma.py
│   ├── retrieval/{vector_retriever,bm25_retriever,hybrid_retriever,fusion,reranker}.py
│   ├── generation/{llm,prompts,citations,abstention}.py
│   ├── rag/pipeline.py
│   └── evaluation/{datasets,retrieval_metrics,generation_metrics,runner}.py
├── data/{raw/zx_bank/, evaluation/golden_dataset.json}
├── vectorstore/chroma/
├── prompts/v1/{system.txt,answer.txt}
├── tests/{unit,integration,api}/
├── scripts/{inspect_dataset,list_chunks,ingest,ask,evaluate,check_quality_gate}.py
├── frontend/app.py
├── docs/
├── .github/workflows/{tests.yml,rag-evaluation.yml}
├── Dockerfile, docker-compose.yml
├── requirements.txt, pytest.ini, .env.example, .gitignore
```

## Installation

```bash
git clone <your-repo-url>
cd zx-bank-rag
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
```

## Environment Variables

```
LLM_PROVIDER=groq
LLM_API_KEY=your-groq-key
LLM_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PATH=./vectorstore/chroma
TOP_K=5
CHUNK_SIZE=600
CHUNK_OVERLAP=100
ABSTENTION_THRESHOLD=<tune from your evaluation numbers>
```

Get a free Groq API key at `console.groq.com/keys`.

## Running the Project

```bash
# 1. Build the index
python -m scripts.ingest

# 2. Ask a question from the CLI
python -m scripts.ask "What are the eligibility requirements for a house loan?"

# 3. Run the API
uvicorn app.main:app --reload

# 4. Run the UI (separate terminal)
streamlit run frontend/app.py
```

Or with Docker: `docker compose up --build`.

## Example Queries

| Type | Example |
|---|---|
| Descriptive | "What is ZX Bank's house loan?" |
| Procedural | "How can a customer apply for a house loan?" |
| Comparative | "What is the difference between the two loan options?" |
| Boolean | "Does ZX Bank provide this service?" |
| Unsupported (tests abstention) | "What is ZX Bank's stock price tomorrow?" |

## Citation System

Every answer must cite sources using `[1]`, `[2]` markers matching numbered context. Citations are built from real chunk metadata (`document_id`, `source`, `section`), never generated by the LLM — see `docs/ingestion.md`. `app/generation/citations.py` flags out-of-range or missing citations after generation.

## Hybrid Retrieval

Vector search (semantic) + BM25 (keyword) combined with Reciprocal Rank Fusion. See `docs/retrieval.md`.

## Reranking

A cross-encoder rescoring the top hybrid candidates for precision, and doubling as the confidence signal for abstention. See `docs/reranking.md`.

## Abstention

Score-based, not LLM self-reported: if the reranker's top score is below `ABSTENTION_THRESHOLD`, the pipeline returns a refusal message without calling the LLM at all. See `docs/decisions.md`.

## Evaluation

Golden dataset (`data/evaluation/golden_dataset.json`) scored on Recall@K, Precision@K, MRR, Faithfulness, Answer Relevance, and Abstention Accuracy. Run `python -m scripts.evaluate`. Full detail in `docs/evaluation.md`.

## Experimental Results

See `docs/experiments.md` for the vector-only vs. BM25-only vs. hybrid vs. hybrid+reranker comparison, with real measured numbers.

## API

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Liveness check |
| `/chat` | POST | `{"question": "..."}` → answer, citations, abstained flag |

Interactive docs at `/docs` once the server is running.

## Testing

```bash
pytest -v
```

Unit tests for parsing, chunking, RRF fusion, reranking (mocked model), and citation validation; integration tests for the ingestion and RAG pipelines (mocked retrieval/LLM); API tests via FastAPI's `TestClient`. No network or live API key required to run the suite.

## Docker

```bash
docker compose up --build
```
API at `localhost:8000`, UI at `localhost:8501`. The vector store and data directories are mounted as volumes, not baked into the image.

## CI/CD

- `.github/workflows/tests.yml` — lint (ruff) + full test suite on every push/PR
- `.github/workflows/rag-evaluation.yml` — on PRs, rebuilds the index and runs `scripts/check_quality_gate.py`, failing the build if Recall@K, MRR, or Faithfulness drop below their measured-baseline thresholds

## Security

API keys via environment variables only, never committed. Retrieved documents are explicitly labeled as untrusted reference material in the system prompt to mitigate prompt injection. Full detail in `docs/security.md`.



## Limitations

- Single corpus, no multi-user document access control
- No API-layer rate limiting yet
- Faithfulness/relevance judge uses the same model family as the generator (self-evaluation bias)
- CI evaluation can be mildly flaky due to LLM non-determinism

## Future Improvements

- Query rewriting for underspecified questions
- PostgreSQL + pgvector for production-scale storage
- React/Next.js frontend
- Observability dashboard (latency, abstention rate, query volume)
- Prompt versioning (v2/v3) with measured impact on evaluation scores
- PDF/DOCX/PPTX ingestion support
- Independent judge model for generation metrics

## Lessons Learned

- LLM provider model IDs are not guaranteed available per API key — always keep the provider abstracted and fail with a clear error, not a raw SDK traceback.
- Fast-moving evaluation libraries (RAGAS) are a real integration risk; custom deterministic metrics you fully control are worth building even when a library nominally does the same thing.
- Score-based abstention is meaningfully more trustworthy than asking an LLM to self-report uncertainty.


## Author

Shanmukha Sriram Poluparthi

## License

`<MIT>`
