from app.embeddings.embedder import embed_texts
from app.vectorstore.chroma import get_collection


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    results = get_collection().query(query_embeddings=embed_texts([query]), n_results=top_k)

    return [
        {
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]