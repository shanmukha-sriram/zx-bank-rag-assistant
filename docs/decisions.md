# Engineering Decision Log

## Decision: ChromaDB for the vector store
**Reason:** zero-infrastructure local persistence, sufficient for this corpus size, gets a working RAG loop running fast.
**Alternative considered:** PostgreSQL + pgvector.
**Why not (yet):** unnecessary operational complexity for a single-corpus project at this stage — a production extension path, not a rejection.

## Decision: Groq as the LLM provider
**Reason:** free developer tier, very low latency, OpenAI-compatible SDK.
**Trade-off:** model availability varies by account/key — during development, `llama-3.3-70b-versatile` returned a `model_not_found` error on one API key while `llama-3.1-8b-instant` and `openai/gpt-oss-120b` worked fine. The app never assumes a specific model is guaranteed available; `LLM_MODEL` is always env-driven, and Groq errors are caught and wrapped (`app/generation/llm.py`) rather than surfaced as raw SDK exceptions.
**Alternative considered:** Gemini, local Ollama models.
**Why abstracted:** the `if provider == "groq"` branch in `app/generation/llm.py` is the entire surface area that would need to change to add another provider — a deliberate design constraint from the start.

## Decision: `sentence-transformers/all-MiniLM-L6-v2` for embeddings
**Reason:** free, runs locally, fast enough for this corpus size, no API key or rate limits to manage.
**Trade-off:** lower ceiling on embedding quality than a larger hosted model; acceptable for the current corpus, revisit if recall plateaus.

## Decision: Custom LLM-as-judge metrics instead of RAGAS
**Reason:** RAGAS's custom-LLM integration API has changed meaningfully across recent versions; building faithfulness/relevance scoring directly on the already-working `generate()` function avoided betting the evaluation layer on a fast-moving third-party API surface.
**Known limitation:** the judge is the same model family that generates the answer — self-evaluation bias is real and not solved, only documented. A stronger or independent judge model is a legitimate future improvement.
**RAGAS status:** kept as an optional, separately-run addition (`docs/evaluation.md`), not load-bearing for the CI quality gate.

## Decision: Word-count chunk sizing instead of a real tokenizer
**Reason:** avoided adding a tokenizer dependency purely for chunk-size estimation; word count is a documented approximation (~1.3 tokens/word), not a precision requirement.

## Decision: Score-based abstention, not LLM self-reporting
**Reason:** an LLM saying "I don't know" is a request to the model's honesty; gating on the reranker's own confidence score means the system can refuse to even call the LLM when evidence is weak — cheaper and more reliably safe.
**Threshold:** currently `<fill in your tuned value>`, set from real evaluation numbers (`docs/evaluation.md`), not guessed.

## Known limitation: CI evaluation flakiness
The RAG evaluation quality gate calls a real LLM twice per example (judge calls) — LLM output isn't perfectly deterministic even at low temperature, so a PR very close to a threshold can occasionally flip pass/fail on rerun. Documented rather than hidden; mitigations (wider margins below baseline, majority-of-N judge calls) are a future improvement, not yet implemented.
