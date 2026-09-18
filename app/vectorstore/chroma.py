import os
from functools import lru_cache
import chromadb


@lru_cache(maxsize=1)
def get_client():
    return chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", "./vectorstore/chroma"))


def get_collection(name: str = "zx_bank"):
    return get_client().get_or_create_collection(name=name)


def add_chunks(chunks, embeddings) -> None:
    get_collection().add(
        ids=[c.chunk_id for c in chunks],
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[
            {
                "document_id": c.document_id,
                "source": c.source,
                "section": c.section,
                "heading_path": c.heading_path,
            }
            for c in chunks
        ],
    )