from app.ingestion.parser import Section
from app.ingestion.chunker import chunk_document


def test_short_section_becomes_one_chunk():
    section = Section("Eligibility", 2, "House Loan > Eligibility", "Short content.")
    chunks = chunk_document("zx-house-loan", "ZX Bank House Loan.md", [section])
    assert len(chunks) == 1


def test_long_section_splits_with_overlap():
    long_text = " ".join(f"word{i}" for i in range(1500))
    section = Section("Terms", 2, "House Loan > Terms", long_text)
    chunks = chunk_document("zx-house-loan", "ZX Bank House Loan.md", [section], chunk_size=600, overlap=100)
    assert len(chunks) > 1
    assert chunks[0].text.split()[-1] in chunks[1].text.split()[:100]


def test_chunk_metadata_is_preserved():
    section = Section("Eligibility", 2, "House Loan > Eligibility", "Some content.")
    chunk = chunk_document("zx-house-loan", "ZX Bank House Loan.md", [section])[0]
    assert chunk.document_id == "zx-house-loan"
    assert chunk.heading_path == "House Loan > Eligibility"