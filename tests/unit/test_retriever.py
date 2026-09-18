from app.retrieval import reranker


def test_rerank_orders_by_score(monkeypatch):
    class FakeCrossEncoder:
        def predict(self, pairs):
            return [0.1, 0.9]

    monkeypatch.setattr(reranker, "_get_model", lambda: FakeCrossEncoder())

    chunks = [{"chunk_id": "a", "text": "irrelevant"}, {"chunk_id": "b", "text": "relevant"}]
    result = reranker.rerank("query", chunks, top_k=2)

    assert result[0]["chunk_id"] == "b"


def test_rerank_handles_empty_input():
    assert reranker.rerank("query", [], top_k=5) == []