from fastapi.testclient import TestClient
from src.chatbot import Chatbot
from src.songchatbot import app
from src.songlibrary import SongLibrary

client = TestClient(app)


# --- Chatbot-Gesprächsfluss ---

class TestChatbotFlow:
    def test_step1_returns_song(self):
        bot = Chatbot()
        response = bot.process_message("love pop slow sad")
        assert "Someone Like You" in response

    def test_step2_nein_shows_next_song(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        response = bot.process_message("nein")
        assert "Score" in response or "Keine passenden Songs" in response

    def test_step2_ja_no_playlists_asks_new_search(self):
        """Ohne Playlists: 'ja' -> direkt zu Schritt 3."""
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        response = bot.process_message("ja")
        assert "Neue Suche" in response
        assert bot.step == 3

    def test_step2_ja_with_playlists_asks_playlist(self):
        """Mit Playlists: 'ja' -> Schritt 4 (Playlist-Angebot)."""
        SongLibrary.create_playlist("favorites")
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        response = bot.process_message("ja")
        assert "Playlist" in response or "speichern" in response
        assert bot.step == 4

    def test_step4_ja_asks_which_playlist(self):
        SongLibrary.create_playlist("favorites")
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")           # -> Schritt 4
        response = bot.process_message("ja")  # -> Schritt 5
        assert "favorites" in response
        assert bot.step == 5

    def test_step4_nein_goes_to_new_search(self):
        SongLibrary.create_playlist("favorites")
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")           # -> Schritt 4
        response = bot.process_message("nein")
        assert "Neue Suche" in response or "nein" in response.lower()
        assert bot.step == 3

    def test_step5_valid_playlist_saves_and_resets(self):
        SongLibrary.create_playlist("favorites")
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")           # -> Schritt 4
        bot.process_message("ja")           # -> Schritt 5
        response = bot.process_message("favorites")
        assert "hinzugefügt" in response or "gespeichert" in response.lower()
        assert bot.step == 3

    def test_step5_invalid_playlist_stays(self):
        SongLibrary.create_playlist("favorites")
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")
        bot.process_message("ja")
        response = bot.process_message("unknown_playlist")
        assert bot.step == 3  # fällt zurück auf Schritt 3

    def test_step3_neu_resets_and_starts_again(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")           # -> Schritt 3 (keine Playlists)
        response = bot.process_message("neu")
        assert "Neue Suche gestartet" in response
        assert bot.step == 1

    def test_step3_nein_says_goodbye(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")
        response = bot.process_message("nein")
        assert "nächsten Mal" in response

    def test_no_matching_songs_returns_error(self):
        bot = Chatbot()
        response = bot.process_message("xyzunknown")
        assert "Keine passenden Songs" in response

    def test_reset_restores_initial_state(self):
        bot = Chatbot()
        bot.process_message("party edm fast energetic")
        bot.reset()
        assert bot.step == 1
        assert bot.results == []
        assert bot.index == 0
        assert bot.current_song is None

    def test_current_song_set_after_step1(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        assert bot.current_song is not None
        assert bot.current_song.title == "Someone Like You"

