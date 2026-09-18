def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    if not relevant_ids:
        return 0.0
    return len(set(retrieved_ids) & set(relevant_ids)) / len(relevant_ids)


def precision_at_k(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    if not retrieved_ids:
        return 0.0
    return len(set(retrieved_ids) & set(relevant_ids)) / len(retrieved_ids)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            return 1.0 / rank
    return 0.0