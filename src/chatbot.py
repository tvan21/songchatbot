import re
from song import Song


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
    return sorted(results, key=lambda item: item[0], reverse=True)


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

        if self.step == 2:
            if text.lower() in ["ja", "j", "yes", "y"]:
                self.step = 3
                return "🎉 Super! Neue Suche starten? (neu / nein)"
            if text.lower() in ["nein", "n", "no"]:
                self.index += 1
                return self.show_song()
            return "Bitte antworte mit ja oder nein 😊"

        if self.step == 3:
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
            return "Bis zum nächsten Mal! 👋"

        self.reset()
        return "❌ Keine passenden Songs gefunden."

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