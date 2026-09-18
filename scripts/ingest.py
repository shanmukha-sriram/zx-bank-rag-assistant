from pathlib import Path
from dotenv import load_dotenv

from app.ingestion.loader import load_markdown_documents
from app.ingestion.cleaner import clean_text
from app.ingestion.parser import parse_sections
from app.ingestion.chunker import chunk_document
from app.embeddings.embedder import embed_texts
from app.vectorstore.chroma import add_chunks, get_collection

DATA_DIR = Path("data/raw/zx_bank")


def main():
    load_dotenv()

    documents = load_markdown_documents(DATA_DIR)
    print(f"Loaded {len(documents)} documents")

    all_chunks = []
    for doc in documents:
        sections = parse_sections(clean_text(doc.raw_text))
        all_chunks.extend(chunk_document(doc.document_id, doc.source, sections))
    print(f"Created {len(all_chunks)} chunks")

    embeddings = embed_texts([c.text for c in all_chunks])
    print(f"Generated {len(embeddings)} embeddings")

    add_chunks(all_chunks, embeddings)
    print(f"Collection now has {get_collection().count()} chunks stored")


if __name__ == "__main__":
    main()