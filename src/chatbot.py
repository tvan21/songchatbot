try:
    from .songlibrary import SongLibrary
except ImportError:
    from songlibrary import SongLibrary

analyze_input = SongLibrary.analyze_input
ranked_songs = SongLibrary.ranked_songs


class Chatbot:
    def __init__(self):
        self.reset()

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
                playlists = SongLibrary.get_playlists()
                if playlists:
                    self.step = 4
                    return f"🔥 Super! Soll ich '{self.current_song.title}' in eine Playlist speichern? (ja/nein)"
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

        if self.step == 4:
            if text.lower() in ["ja", "j", "yes", "y"]:
                playlists = SongLibrary.get_playlists()
                self.step = 5
                return f"In welche Playlist? 📂\nVerfügbar: {', '.join(playlists)}"
            self.step = 3
            return "Alles klar! Neue Suche starten? (neu / nein)"

        if self.step == 5:
            success = SongLibrary.add_to_playlist(text, self.current_song.title)
            self.step = 3
            if success:
                return f"✅ '{self.current_song.title}' wurde zu '{text}' hinzugefügt!\nNeue Suche starten? (neu / nein)"
            return "Diese Playlist kenne ich nicht. Neue Suche starten? (neu / nein)"

        self.reset()
        return "❌ Keine passenden Songs gefunden."

    def show_song(self):
        if self.index >= len(self.results) or self.results[self.index][0] == 0:
            self.reset()
            return "❌ Keine passenden Songs gefunden."

        score, song = self.results[self.index]
        self.current_song = song
        artist_info = f" von {song.artist}" if song.artist else ""
        return f"🎵 {song.title}{artist_info} (Score: {score})\n\nGefällt dir der Song? (ja/nein)"

    def reset(self):
        self.step = 1
        self.results = []
        self.index = 0
        self.current_song = None

        self.results = []
        self.index = 0