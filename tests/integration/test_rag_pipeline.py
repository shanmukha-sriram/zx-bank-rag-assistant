from app.rag import pipeline

FAKE_CHUNK = {
    "chunk_id": "zx-house-loan-eligibility-00",
    "text": "Applicants must be 21 or older.",
    "metadata": {"source": "ZX Bank House Loan.md", "section": "Eligibility"},
    "rerank_score": 5.0,
}


def test_pipeline_returns_answer_with_sources(monkeypatch):
    monkeypatch.setattr(pipeline, "hybrid_retrieve", lambda q, top_k=20: [FAKE_CHUNK])
    monkeypatch.setattr(pipeline, "rerank", lambda q, chunks, top_k=5: [FAKE_CHUNK])
    monkeypatch.setattr(pipeline, "generate", lambda system, user: "Must be 21 or older. [1]")

    result = pipeline.answer_question("What are the eligibility requirements?")

    assert result["abstained"] is False
    assert result["sources"] == [{"source": "ZX Bank House Loan.md", "section": "Eligibility"}]


def test_pipeline_abstains_when_no_evidence(monkeypatch):
    monkeypatch.setattr(pipeline, "hybrid_retrieve", lambda q, top_k=20: [])
    monkeypatch.setattr(pipeline, "rerank", lambda q, chunks, top_k=5: [])

    result = pipeline.answer_question("What is ZX Bank's stock price tomorrow?")
    assert result["abstained"] is True