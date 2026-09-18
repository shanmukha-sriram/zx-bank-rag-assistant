import time
import uuid

from app.core.logging import get_logger
from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.retrieval.reranker import rerank
from app.generation.llm import generate
from app.generation.prompts import load_system_prompt, build_user_prompt
from app.generation.abstention import is_evidence_sufficient, ABSTENTION_MESSAGE
from app.generation.citations import validate_citations

logger = get_logger(__name__)


def _reformulate_query(question: str, history: list[dict]) -> str:
    """Combines history + question into a standalone search query if history exists."""
    if not history:
        return question

    past_user_msgs = [m.get("content", "") for m in history if m.get("role") == "user"]
    if past_user_msgs:
        recent_context = past_user_msgs[-1]
        prompt = (
            f"Given the conversation topic: '{recent_context}', rewrite the follow-up "
            f"question '{question}' into a single specific search query. Output ONLY the search query:"
        )
        return generate("You are a search query optimizer.", prompt).strip()
    return question


def answer_question(
    question: str,
    history: list[dict] = None,
    candidate_k: int = 90,
    top_k: int = 5
) -> dict:
    request_id = str(uuid.uuid4())[:8]
    history = history or []
    logger.info(f"[{request_id}] query='{question}' history_len={len(history)}")

    # 1. Reformulate search query using history context for follow-up questions
    search_query = _reformulate_query(question, history)
    if search_query != question:
        logger.info(f"[{request_id}] reformulated_query='{search_query}'")

    # 2. Hybrid retrieve & rerank with performance timing
    t0 = time.perf_counter()
    candidates = hybrid_retrieve(search_query, top_k=candidate_k)
    chunks = rerank(search_query, candidates, top_k=top_k)
    retrieval_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"[{request_id}] chunks={len(chunks)} retrieval_ms={retrieval_ms:.0f}")

    # 3. Evidence check / Abstention gate
    if not is_evidence_sufficient(chunks):
        logger.info(f"[{request_id}] abstained=True")
        return {
            "answer": ABSTENTION_MESSAGE,
            "sources": [],
            "abstained": True,
            "citation_warnings": [],
        }

    # 4. Generate grounded response with timing
    t1 = time.perf_counter()
    user_prompt = build_user_prompt(question, chunks, history=history)
    answer_text = generate(load_system_prompt(), user_prompt)
    llm_ms = (time.perf_counter() - t1) * 1000
    logger.info(f"[{request_id}] llm_ms={llm_ms:.0f}")

    # 5. Extract sources & Validate citations
    sources = [
        {
            "source": c.get("metadata", {}).get("source", "Unknown Document"),
            "section": c.get("metadata", {}).get("section", "General"),
        }
        for c in chunks
    ]

    warnings = validate_citations(answer_text, len(chunks))
    if warnings:
        logger.warning(f"[{request_id}] citation_warnings={warnings}")

    return {
        "answer": answer_text,
        "sources": sources,
        "abstained": False,
        "citation_warnings": warnings,
    }