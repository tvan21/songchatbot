import sqlite3
from pathlib import Path
from src.songlibrary import SongLibrary, DB_PATH

class TestSongLibrary:

    def test_init_db_creates_tables(self):
        SongLibrary.init_db()
        conn = sqlite3.connect(DB_PATH)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        conn.close()
        assert ("songs",) in tables

    def test_seed_db_loads_initial_songs(self):
        SongLibrary.init_db()
        songs = SongLibrary.load_songs()
        assert len(songs) == 15

    def test_add_and_load_song(self):
        SongLibrary.add_song("Test Song", "Test Artist", "pop", "fast", "happy", "test,keyword")
        songs = SongLibrary.load_songs()
        assert any(s.title == "Test Song" for s in songs)