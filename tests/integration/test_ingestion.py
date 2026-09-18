from pathlib import Path
from app.ingestion.loader import load_markdown_documents
from app.ingestion.cleaner import clean_text
from app.ingestion.parser import parse_sections
from app.ingestion.chunker import chunk_document


def test_full_ingestion_pipeline(tmp_path: Path):
    (tmp_path / "sample.md").write_text("# Sample Loan\n\n## Eligibility\n\nMust be 21.\n", encoding="utf-8")

    documents = load_markdown_documents(tmp_path)
    doc = documents[0]
    sections = parse_sections(clean_text(doc.raw_text))
    chunks = chunk_document(doc.document_id, doc.source, sections)

    assert len(chunks) >= 1
    assert chunks[0].heading_path.startswith("Sample Loan")