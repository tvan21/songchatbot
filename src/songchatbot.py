from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chatbot import Chatbot

HTML_FILE = Path(__file__).parent / "static" / "index.html"

app = FastAPI(
    title="🎵 Song-Chatbot Web",
    description="Webbasierter Song-Chatbot",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_FILE.read_text(encoding="utf-8")

# Globale Chatbot-Instanz
chatbot = Chatbot()


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

WELCOME_TEXT = "🎵 Willkommen!\nBeschreibe einfach, was du hören möchtest."

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chatbot.process_message(request.message)
    return ChatResponse(response=response)

@app.post("/reset")
def reset():
    chatbot.reset()
    return {"status": "reset erfolgreich"}

if __name__ == "__main__":
    import threading
    import webbrowser
    import uvicorn

    def open_browser():
        webbrowser.open("http://localhost:8000")

    threading.Timer(1.0, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")