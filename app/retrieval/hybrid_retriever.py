from app.retrieval.vector_retriever import retrieve as vector_retrieve
from app.retrieval.bm25_retriever import retrieve_bm25
from app.retrieval.fusion import reciprocal_rank_fusion


def hybrid_retrieve(query: str, top_k: int = 20) -> list[dict]:
    vector_results = vector_retrieve(query, top_k=top_k)
    bm25_results = retrieve_bm25(query, top_k=top_k)

    lookup = {c["chunk_id"]: c for c in vector_results}
    lookup.update({c["chunk_id"]: c for c in bm25_results if c["chunk_id"] not in lookup})

    fused = reciprocal_rank_fusion(
        [[c["chunk_id"] for c in vector_results], [c["chunk_id"] for c in bm25_results]]
    )
    ranked_ids = sorted(fused, key=lambda cid: fused[cid], reverse=True)
    return [lookup[cid] for cid in ranked_ids]