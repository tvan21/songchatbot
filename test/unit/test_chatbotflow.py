from fastapi.testclient import TestClient
from src.chatbot import Chatbot
from src.songchatbot import app

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

    def test_step2_ja_asks_for_new_search(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        response = bot.process_message("ja")
        assert "Neue Suche" in response

    def test_step3_neu_resets_and_starts_again(self):
        bot = Chatbot()
        bot.process_message("love pop slow sad")
        bot.process_message("ja")
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

