import os

DEFAULT_THRESHOLD = 0.0  # provisional — we'll tune this properly with real data on Day 4

ABSTENTION_MESSAGE = (
    "I couldn't find sufficient information in the ZX Bank documents to answer this question."
)


def is_evidence_sufficient(chunks: list[dict]) -> bool:
    if not chunks:
        return False
    threshold = float(os.getenv("ABSTENTION_THRESHOLD", DEFAULT_THRESHOLD))
    best_score = max(c.get("rerank_score", float("-inf")) for c in chunks)
    return best_score >= threshold