import unittest
from src.chatbot import analyze_input

class TestAnalyzeInput(unittest.TestCase):

    def test_analyze_input_basic(self):
        input_text = "NIGHT, POP, FAST, HAPPY"
        expected_output = ('night', 'pop', 'fast', 'happy')
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_lowercase(self):
        input_text = "love pop slow sad"
        expected_output = ('love', 'pop', 'slow', 'sad')
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_synonyms(self):
        input_text = "party edm fast lively"
        expected_output = ('party', 'edm', 'fast', 'energetic')  
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_only_keyword(self):
        input_text = "sunset"
        expected_output = ('sunset', '', '', '')
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_only_genre(self):
        input_text = "rock"
        expected_output = ('', 'rock', '', '')
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_empty_string(self):
        input_text = ""
        expected_output = ('', '', '', '')
        self.assertEqual(analyze_input(input_text), expected_output)

    def test_analyze_input_multiple_keywords(self):
        input_text = "sunset sunrise"
        expected_output = ('sunrise', '', '', '')
        self.assertEqual(analyze_input(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()