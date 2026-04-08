import unittest
from src.chatbot import ranked_songs
from src.song import Song


class TestRankedSongs(unittest.TestCase):

    def setUp(self):
        # Test-Songliste mit 5 Songs (song_list explizit übergeben – kein DB-Zugriff)
        self.test_songs = [
            Song("Song A", ["love"], "pop", "fast", "happy"),
            Song("Song B", ["love"], "pop", "slow", "sad"),
            Song("Song C", ["party"], "edm", "fast", "energetic"),
            Song("Song D", ["love"], "pop", "fast", "sad"),
            Song("Song E", ["night"], "rock", "medium", "moody"),
        ]

    def test_sorted_by_score(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        scores = [score for score, song in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_best_song_first(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        self.assertEqual(ranked[0][1].title, "Song A")

    def test_second_song(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        self.assertEqual(ranked[1][1].title, "Song D")

    def test_list_length(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        self.assertEqual(len(ranked), 5)

    def test_empty_song_list_uses_db(self):
        # DB wird von conftest-Fixture initialisiert und mit Seed-Songs befüllt
        ranked = ranked_songs("love", "pop", "fast", "happy")
        self.assertGreater(len(ranked), 0)
        self.assertEqual(ranked[0][1].title, "Blinding Lights")

    def test_scores_not_negative(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        for score, song in ranked:
            self.assertGreaterEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
