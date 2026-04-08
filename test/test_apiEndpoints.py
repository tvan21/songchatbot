from fastapi.testclient import TestClient
from src.chatbot import Chatbot
from src.songchatbot import app

client = TestClient(app)


# --- FastAPI-Endpoints ---

class TestApiEndpoints:

    # ── /chat & /reset ────────────────────────────────────────────────────────

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

    # ── GET /songs ────────────────────────────────────────────────────────────

    def test_get_songs_returns_list(self):
        r = client.get("/songs")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_songs_contains_seeded_songs(self):
        r = client.get("/songs")
        titles = [s["title"] for s in r.json()]
        assert "Blinding Lights" in titles

    def test_get_songs_fields(self):
        r = client.get("/songs")
        song = r.json()[0]
        assert "title" in song
        assert "artist" in song
        assert "genre" in song
        assert "tempo" in song
        assert "mood" in song
        assert "keywords" in song

    # ── POST /songs ───────────────────────────────────────────────────────────

    def test_post_song_created(self):
        r = client.post("/songs", json={
            "title": "Test Song",
            "artist": "Test Artist",
            "genre": "pop",
            "tempo": "fast",
            "mood": "happy",
            "keywords": "test,new"
        })
        assert r.status_code == 201
        assert r.json()["title"] == "Test Song"

    def test_post_song_appears_in_list(self):
        client.post("/songs", json={
            "title": "Unique Track",
            "artist": "Someone",
            "genre": "jazz",
            "tempo": "slow",
            "mood": "cool",
            "keywords": "unique,jazz"
        })
        r = client.get("/songs")
        titles = [s["title"] for s in r.json()]
        assert "Unique Track" in titles

    # ── GET /playlists ────────────────────────────────────────────────────────

    def test_get_playlists_empty(self):
        r = client.get("/playlists")
        assert r.status_code == 200
        assert "playlists" in r.json()
        assert isinstance(r.json()["playlists"], list)

    # ── POST /playlists ───────────────────────────────────────────────────────

    def test_create_playlist(self):
        r = client.post("/playlists", json={"name": "meine-liste"})
        assert r.status_code == 201
        assert r.json()["name"] == "meine-liste"

    def test_created_playlist_appears_in_list(self):
        client.post("/playlists", json={"name": "meine-liste"})
        r = client.get("/playlists")
        assert "meine-liste" in r.json()["playlists"]

    # ── GET /playlists/{name} ─────────────────────────────────────────────────

    def test_get_playlist_songs_empty(self):
        client.post("/playlists", json={"name": "leer"})
        r = client.get("/playlists/leer")
        assert r.status_code == 200
        assert r.json()["songs"] == []

    def test_get_playlist_not_found(self):
        r = client.get("/playlists/doesnotexist")
        assert r.status_code == 404

    # ── POST /playlists/{name}/songs ──────────────────────────────────────────

    def test_add_song_to_playlist(self):
        client.post("/playlists", json={"name": "favs"})
        r = client.post("/playlists/favs/songs", json={"song_title": "Blinding Lights"})
        assert r.status_code == 200

    def test_add_song_to_playlist_appears_in_songs(self):
        client.post("/playlists", json={"name": "favs"})
        client.post("/playlists/favs/songs", json={"song_title": "Blinding Lights"})
        r = client.get("/playlists/favs")
        titles = [s["title"] for s in r.json()["songs"]]
        assert "Blinding Lights" in titles

    def test_add_song_to_nonexistent_playlist_returns_404(self):
        r = client.post("/playlists/ghost/songs", json={"song_title": "Blinding Lights"})
        assert r.status_code == 404

