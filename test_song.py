import unittest
from songchatbot import Song

class TestSongClass(unittest.TestCase):
    def setUp(self): self.song = Song( title="Test Song", keywords=["love", "summer", "party"], genre="pop", tempo="fast", mood="happy" )
    
    def test_score_all_match(self):
        self.assertEqual(
            self.song.score("love", "pop", "fast", "happy"),
            5
        )

    def test_score_only_keyword(self):
        self.assertEqual(
            self.song.score("summer", None, None, None),
            2
        )

    def test_score_genre_and_mood(self):
        self.assertEqual(
            self.song.score(None, "pop", None, "happy"),
            2
        )

    def test_score_no_match(self):
        self.assertEqual(
            self.song.score("rock", "rock", "slow", "sad"),
            0
        )

if __name__ == '__main__':    unittest.main()