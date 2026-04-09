# conftest.py
import sys
import os
import pytest
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(autouse=True)
def temp_db(monkeypatch, tmp_path):
    """Jeder Test bekommt eine frische, isolierte In-Memory-äquivalente DB."""
    db_file = tmp_path / "test_songs.db"
    import src.songlibrary as sl
    monkeypatch.setattr(sl, "DB_PATH", db_file)
    sl.SongLibrary.init_db()
    yield db_file