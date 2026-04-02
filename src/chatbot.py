try:
    from .songlibrary import SongLibrary
except ImportError:
    from songlibrary import SongLibrary

analyze_input = SongLibrary.analyze_input
ranked_songs = SongLibrary.ranked_songs


class Chatbot:
    def __init__(self):
        self.step = 1
        self.results = []
        self.index = 0

    def process_message(self, user_input):
        text = user_input.strip()

        if self.step == 1:
            keyword, genre, tempo, mood = SongLibrary.analyze_input(text)
            self.results = SongLibrary.ranked_songs(keyword, genre, tempo, mood)
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