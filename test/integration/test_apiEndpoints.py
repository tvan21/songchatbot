from fastapi.testclient import TestClient
from src.chatbot import Chatbot
from src.songchatbot import app

client = TestClient(app)
# --- FastAPI-Endpoints ---

class TestApiEndpoints:
    def test_chat_endpoint_returns_response(self):
        r = client.post("/chat", json={"message": "love pop slow sad"})
        assert r.status_code == 200
        assert "response" in r.json()
        assert isinstance(r.json()["response"], str)

    def test_chat_endpoint_content(self):
        r = client.post("/chat", json={"message": "party edm fast energetic"})
        assert r.status_code == 200
        assert len(r.json()["response"]) > 0

    def test_reset_endpoint(self):
        r = client.post("/reset")
        assert r.status_code == 200
        assert r.json()["status"] == "reset erfolgreich"

    def test_chat_after_reset(self):
        client.post("/reset")
        r = client.post("/chat", json={"message": "love pop slow sad"})
        assert r.status_code == 200
        assert "Score" in r.json()["response"]

    def test_index_returns_html(self):
        r = client.get("/")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
