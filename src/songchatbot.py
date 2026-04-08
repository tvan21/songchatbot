from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
try:
    from .chatbot import Chatbot
    from .songlibrary import SongLibrary
except ImportError:
    from chatbot import Chatbot
    from songlibrary import SongLibrary

HTML_FILE = Path(__file__).parent / "static" / "index.html"

app = FastAPI(
    title="🎵 Song-Chatbot Web",
    description="Webbasierter Song-Chatbot",
    version="2.0.0"
)


@app.on_event("startup")
def startup():
    SongLibrary.init_db()


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_FILE.read_text(encoding="utf-8")


# Globale Chatbot-Instanz
chatbot = Chatbot()


# ------------------------------------------------------------------
# Chat
# ------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chatbot.process_message(request.message)
    return ChatResponse(response=response)

@app.post("/reset")
def reset():
    chatbot.reset()
    return {"status": "reset erfolgreich"}


# ------------------------------------------------------------------
# Songs
# ------------------------------------------------------------------

class SongIn(BaseModel):
    title: str
    artist: str
    genre: str
    tempo: str
    mood: str
    keywords: str  # kommagetrennt

class SongOut(BaseModel):
    title: str
    artist: str
    genre: str
    tempo: str
    mood: str
    keywords: List[str]

@app.get("/songs", response_model=List[SongOut])
def get_songs():
    return [
        SongOut(title=s.title, artist=s.artist, genre=s.genre,
                tempo=s.tempo, mood=s.mood, keywords=s.keywords)
        for s in SongLibrary.load_songs()
    ]

@app.post("/songs", status_code=201)
def add_song(song: SongIn):
    SongLibrary.add_song(song.title, song.artist, song.genre,
                         song.tempo, song.mood, song.keywords)
    return {"status": "Song gespeichert", "title": song.title}


# ------------------------------------------------------------------
# Playlists
# ------------------------------------------------------------------

class PlaylistIn(BaseModel):
    name: str

class PlaylistSongIn(BaseModel):
    song_title: str

@app.get("/playlists")
def get_playlists():
    return {"playlists": SongLibrary.get_playlists()}

@app.post("/playlists", status_code=201)
def create_playlist(body: PlaylistIn):
    SongLibrary.create_playlist(body.name)
    return {"status": "Playlist erstellt", "name": body.name}

@app.get("/playlists/{name}")
def get_playlist_songs(name: str):
    songs = SongLibrary.get_playlist_songs(name)
    if songs is None:
        raise HTTPException(status_code=404, detail="Playlist nicht gefunden")
    return {"playlist": name, "songs": songs}

@app.post("/playlists/{name}/songs")
def add_song_to_playlist(name: str, body: PlaylistSongIn):
    success = SongLibrary.add_to_playlist(name, body.song_title)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist oder Song nicht gefunden")
    return {"status": "Song zur Playlist hinzugefügt"}


if __name__ == "__main__":
    import threading
    import webbrowser
    import uvicorn

    def open_browser():
        webbrowser.open("http://localhost:8000")

    threading.Timer(1.0, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
