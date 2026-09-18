from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import chat as chat_route


def test_health_endpoint():
    response = TestClient(app).get("/health")
    assert response.status_code == 200


def test_chat_endpoint(monkeypatch):
    fake = {
        "answer": "Must be 21. [1]",
        "sources": [{"source": "House Loan.md", "section": "Eligibility"}],
        "abstained": False,
    }
    # Accept **kwargs to handle additional parameters passed by the route like history
    monkeypatch.setattr(chat_route, "answer_question", lambda question, **kwargs: fake)

    response = TestClient(app).post("/chat", json={"question": "eligibility?"})
    assert response.status_code == 200
    assert response.json()["answer"] == fake["answer"]