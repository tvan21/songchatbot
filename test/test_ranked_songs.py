import unittest
from src.songchatbot import Song, ranked_songs  # Modulname anpassen!


class TestRankedSongs(unittest.TestCase):

    def setUp(self):
        # Test-Songliste mit 5 Songs
        self.test_songs = [
            Song("Song A", ["love"], "pop", "fast", "happy"),      # Score 5
            Song("Song B", ["love"], "pop", "slow", "sad"),        # Score 3
            Song("Song C", ["party"], "edm", "fast", "energetic"), # Score 0
            Song("Song D", ["love"], "pop", "fast", "sad"),        # Score 4
            Song("Song E", ["night"], "rock", "medium", "moody"),  # Score 0
        ]

    def test_sorted_by_score(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)

        # Scores sollten absteigend sortiert sein
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

    def test_empty_song_list(self):
        ranked = ranked_songs("love", "pop", "fast", "happy")
        self.assertEqual(ranked[0][1].title, "Blinding Lights")

    def test_scores_not_negative(self):
        ranked = ranked_songs("love", "pop", "fast", "happy", song_list=self.test_songs)
        for score, song in ranked:
            self.assertGreaterEqual(score, 0)


if __name__ == "__main__":
    unittest.main()
    unittest.main()