import re
import tkinter as tk
from tkinter import scrolledtext

# =========================
# Song-Klasse
# =========================

class Song:
    def __init__(self, title, keywords, genre, tempo, mood):
        self.title = title
        self.keywords = keywords
        self.genre = genre
        self.tempo = tempo
        self.mood = mood

    def score(self, keyword, genre, tempo, mood):
        score = 0
        if keyword and keyword in self.keywords:
            score += 2
        if genre and self.genre == genre:
            score += 1
        if tempo and self.tempo == tempo:
            score += 1
        if mood and self.mood == mood:
            score += 1
        return score


# =========================
# Song-Datenbank
# =========================

songs = [
    Song("Blinding Lights", ["night", "city", "love"], "pop", "fast", "happy"),
    Song("Someone Like You", ["love", "heartbreak"], "pop", "slow", "sad"),
    Song("Lose Yourself", ["motivation", "dream", "fight"], "hiphop", "fast", "energetic"),
    Song("We Will Rock You", ["motivation", "power", "stadium"], "rock", "medium", "energetic"),
    Song("Gasolina", ["party", "dance"], "latin", "fast", "energetic"),
    Song("Clair de Lune", ["calm", "night", "piano"], "classical", "slow", "peaceful"),
    Song("Levels", ["party", "energy", "festival"], "edm", "fast", "energetic"),
    Song("Take Five", ["jazz", "relax", "night"], "jazz", "medium", "cool"),
    Song("No Woman No Cry", ["life", "hope", "freedom"], "reggae", "slow", "warm"),
    Song("The Hills", ["dark", "night", "love"], "rnb", "medium", "moody"),
    Song("Fear of the Dark", ["dark", "fear", "night"], "metal", "fast", "aggressive"),
    Song("River", ["soul", "emotion", "heartbreak"], "soul", "slow", "emotional"),
    Song("Shape of You", ["love", "dance", "night"], "pop", "medium", "romantic"),
    Song("Smells Like Teen Spirit", ["rebellion", "youth"], "rock", "fast", "angry"),
    Song("Blue World", ["chill", "vibes", "thinking"], "lofi", "slow", "relaxed"),
]

# =========================
# Kategorien
# =========================

GENRES = ["pop", "hiphop", "rock", "latin", "edm", "jazz", "reggae", "rnb", "metal", "soul", "classical", "lofi"]
TEMPOS = ["slow", "medium", "fast"]
MOODS = {
    "happy": ["joyful", "glad", "cheerful"],
    "sad": ["unhappy", "down", "blue"],
    "energetic": ["lively", "excited", "active"],
    "peaceful": ["calm", "serene"],
    "moody": ["dark", "gloomy"],
    "angry": ["mad", "furious"],
    "romantic": ["loving", "affectionate"],
    "aggressive": ["fierce", "intense"],
    "emotional": ["touching", "heartfelt"],
    "warm": ["cozy", "friendly"],
    "cool": ["chill", "laid-back"],
}

# =========================
# Analyse & Ranking
# =========================

def analyze_input(text):
    keyword = ""
    genre = ""
    tempo = ""
    mood = ""

    tokens = re.split(r"[,\s]+", text.lower())

    for token in tokens:
        if token in GENRES:
            genre = token
        elif token in TEMPOS:
            tempo = token
        else:
            for standard, synonyms in MOODS.items():
                if token == standard or token in synonyms:
                    mood = standard
                    break
            else:
                if token:
                    keyword = token

    return keyword, genre, tempo, mood


def ranked_songs(keyword, genre, tempo, mood, song_list=None):
    if song_list is None:
        song_list = songs

    results = []
    for song in song_list:
        results.append((song.score(keyword, genre, tempo, mood), song))
    return sorted(results, key=lambda x: x[0], reverse=True)


# =========================
# Chatbot
# =========================

class Chatbot:
    def __init__(self):
        self.step = 1
        self.results = []
        self.index = 0

    def process_message(self, user_input):
        text = user_input.strip()

        if self.step == 1:
            keyword, genre, tempo, mood = analyze_input(text)
            self.results = ranked_songs(keyword, genre, tempo, mood)
            self.index = 0
            self.step = 2
            return self.show_song()

        elif self.step == 2:
            if text.lower() in ["ja", "j", "yes", "y"]:
                self.step = 3
                return "🎉 Super! Neue Suche starten? (neu / nein)"
            elif text.lower() in ["nein", "n", "no"]:
                self.index += 1
                return self.show_song()
            else:
                return "Bitte antworte mit ja oder nein 😊"

        elif self.step == 3:
            if text.lower() in ["neu", "ja", "j", "yes", "y"]:
                self.reset()
                return (
                    "🎵 Neue Suche gestartet!\n"
                    "Beschreibe einfach, was du hören möchtest.\n\n"
                    "Beispiele:\n"
                    "👉 love pop fast happy\n"
                    "👉 party edm energetic\n"
                    "👉 ruhiger jazz song"
                )
            else:
                return "Bis zum nächsten Mal! 👋"

    def show_song(self):
        if self.index >= len(self.results) or self.results[self.index][0] == 0:
            self.reset()
            return "❌ Keine passenden Songs gefunden."

        score, song = self.results[self.index]
        return f"🎵 {song.title} (Score: {score})\n\nGefällt dir der Song? (ja/nein)"

    def reset(self):
        self.step = 1
        self.results = []
        self.index = 0


# =========================
# GUI (DEIN DESIGN)
# =========================

root = tk.Tk()
root.title("🎵 Song-Chatbot")
root.geometry("550x700")
root.configure(bg="#f0f0f5")

chatbot = Chatbot()

header = tk.Frame(root, bg="#7c3aed", height=100)
header.pack(fill=tk.X, padx=10, pady=10)
header.pack_propagate(False)

tk.Label(
    header,
    text="🎵 Song-Chatbot",
    font=("Segoe UI", 20, "bold"),
    bg="#7c3aed",
    fg="white"
).pack(pady=10)

tk.Label(
    header,
    text="Finde deinen perfekten Song",
    font=("Segoe UI", 11),
    bg="#7c3aed",
    fg="#e9d5ff"
).pack()

chat_display = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 10),
    bg="#fafafa",
    state=tk.DISABLED
)
chat_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

entry = tk.Entry(root, font=("Segoe UI", 11))
entry.pack(fill=tk.X, padx=10, pady=10)

def add_message(sender, msg):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"{sender}: {msg}\n\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

def send(event=None):
    msg = entry.get()
    entry.delete(0, tk.END)
    add_message("Du", msg)
    add_message("Bot", chatbot.process_message(msg))

entry.bind("<Return>", send)

add_message(
    "Bot",
    "Willkommen! 🎵\n"
    "Bitte gebe jeweils kommasepariert eine Kategorie, Genre, Tempo(slow/medium/fast), Stimmung an.\n"
)
if __name__ == "__main__":
    root.mainloop()
