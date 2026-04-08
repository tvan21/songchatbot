import re
import sqlite3
from pathlib import Path

try:
    from .song import Song
except ImportError:
    from song import Song

DB_PATH = Path(__file__).parent / "songs.db"

_INITIAL_SONGS = [
    ("Blinding Lights",       "The Weeknd",      ["night", "city", "love"],          "pop",       "fast",   "happy"),
    ("Someone Like You",      "Adele",           ["love", "heartbreak"],              "pop",       "slow",   "sad"),
    ("Lose Yourself",         "Eminem",          ["motivation", "dream", "fight"],    "hiphop",    "fast",   "energetic"),
    ("We Will Rock You",      "Queen",           ["motivation", "power", "stadium"],  "rock",      "medium", "energetic"),
    ("Gasolina",              "Daddy Yankee",    ["party", "dance"],                  "latin",     "fast",   "energetic"),
    ("Clair de Lune",         "Claude Debussy",  ["calm", "night", "piano"],          "classical", "slow",   "peaceful"),
    ("Levels",                "Avicii",          ["party", "energy", "festival"],     "edm",       "fast",   "energetic"),
    ("Take Five",             "Dave Brubeck",    ["jazz", "relax", "night"],          "jazz",      "medium", "cool"),
    ("No Woman No Cry",       "Bob Marley",      ["life", "hope", "freedom"],         "reggae",    "slow",   "warm"),
    ("The Hills",             "The Weeknd",      ["dark", "night", "love"],           "rnb",       "medium", "moody"),
    ("Fear of the Dark",      "Iron Maiden",     ["dark", "fear", "night"],           "metal",     "fast",   "aggressive"),
    ("River",                 "Leon Bridges",    ["soul", "emotion", "heartbreak"],   "soul",      "slow",   "emotional"),
    ("Shape of You",          "Ed Sheeran",      ["love", "dance", "night"],          "pop",       "medium", "romantic"),
    ("Smells Like Teen Spirit","Nirvana",        ["rebellion", "youth"],              "rock",      "fast",   "angry"),
    ("Blue World",            "Mac Miller",      ["chill", "vibes", "thinking"],      "lofi",      "slow",   "peaceful"),
]


class SongLibrary:
    GENRES = ["pop", "hiphop", "rock", "latin", "edm", "jazz", "reggae", "rnb", "metal", "soul", "classical", "lofi"]
    TEMPOS = ["slow", "medium", "fast"]
    MOODS = {
        "happy": ["joyful", "glad", "cheerful"],
        "sad": ["unhappy", "down", "blue"],
        "energetic": ["lively", "excited", "active"],
        "peaceful": ["calm", "serene"],
        "moody": ["dark", "gloomy"],
        "angry": ["mad", "furious"],
        "romantic": ["loving", "affectionate"],
        "aggressive": ["fierce", "intense"],
        "emotional": ["touching", "heartfelt"],
        "warm": ["cozy", "friendly"],
        "cool": ["chill", "laid-back"],
    }

    # ------------------------------------------------------------------
    # DB setup
    # ------------------------------------------------------------------

    @staticmethod
    def init_db():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS tempos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist_id INTEGER,
                genre_id  INTEGER,
                mood_id   INTEGER,
                tempo_id  INTEGER,
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (genre_id)  REFERENCES genres(id),
                FOREIGN KEY (mood_id)   REFERENCES moods(id),
                FOREIGN KEY (tempo_id)  REFERENCES tempos(id));
            CREATE TABLE IF NOT EXISTS song_keywords (
                song_id    INTEGER,
                keyword_id INTEGER,
                PRIMARY KEY (song_id, keyword_id),
                FOREIGN KEY (song_id)    REFERENCES songs(id),
                FOREIGN KEY (keyword_id) REFERENCES keywords(id));
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id INTEGER,
                song_id     INTEGER,
                PRIMARY KEY (playlist_id, song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists(id),
                FOREIGN KEY (song_id)     REFERENCES songs(id));
        """)
        conn.commit()
        conn.close()
        SongLibrary.seed_db()

    @staticmethod
    def seed_db():
        conn = sqlite3.connect(DB_PATH)
        if conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0] == 0:
            conn.close()
            for title, artist, keywords, genre, tempo, mood in _INITIAL_SONGS:
                SongLibrary.add_song(title, artist, genre, tempo, mood, keywords)
        else:
            conn.close()

    # ------------------------------------------------------------------
    # Song CRUD
    # ------------------------------------------------------------------

    @staticmethod
    def add_song(title, artist, genre, tempo, mood, keywords):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        def get_or_create(table, val):
            val = val.strip().lower()
            cur.execute(f"INSERT OR IGNORE INTO {table} (name) VALUES (?)", (val,))
            return cur.execute(f"SELECT id FROM {table} WHERE name=?", (val,)).fetchone()[0]

        try:
            a_id = get_or_create("artists", artist)
            g_id = get_or_create("genres",  genre)
            m_id = get_or_create("moods",   mood)
            t_id = get_or_create("tempos",  tempo)

            cur.execute(
                "INSERT INTO songs (title, artist_id, genre_id, mood_id, tempo_id) VALUES (?,?,?,?,?)",
                (title.strip(), a_id, g_id, m_id, t_id),
            )
            s_id = cur.lastrowid

            kw_list = keywords if isinstance(keywords, list) else [k.strip() for k in keywords.split(",")]
            for kw in kw_list:
                kw = kw.strip().lower()
                if not kw:
                    continue
                cur.execute("INSERT OR IGNORE INTO keywords (word) VALUES (?)", (kw,))
                kw_id = cur.execute("SELECT id FROM keywords WHERE word=?", (kw,)).fetchone()[0]
                cur.execute("INSERT OR IGNORE INTO song_keywords VALUES (?,?)", (s_id, kw_id))

            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def load_songs():
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("""
            SELECT s.title, a.name, g.name, t.name, m.name, GROUP_CONCAT(k.word)
            FROM songs s
            JOIN artists a ON s.artist_id = a.id
            JOIN genres  g ON s.genre_id  = g.id
            JOIN tempos  t ON s.tempo_id  = t.id
            JOIN moods   m ON s.mood_id   = m.id
            LEFT JOIN song_keywords sk ON s.id = sk.song_id
            LEFT JOIN keywords k ON sk.keyword_id = k.id
            GROUP BY s.id
        """).fetchall()
        conn.close()
        return [
            Song(title, kw.split(",") if kw else [], genre, tempo, mood, artist=artist)
            for title, artist, genre, tempo, mood, kw in rows
        ]

    # ------------------------------------------------------------------
    # Playlist CRUD
    # ------------------------------------------------------------------

    @staticmethod
    def get_playlists():
        conn = sqlite3.connect(DB_PATH)
        names = [r[0] for r in conn.execute("SELECT name FROM playlists ORDER BY name").fetchall()]
        conn.close()
        return names

    @staticmethod
    def create_playlist(name):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT OR IGNORE INTO playlists (name) VALUES (?)", (name.strip().lower(),))
        conn.commit()
        conn.close()

    @staticmethod
    def add_to_playlist(playlist_name, song_title):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        pl = conn.execute("SELECT id FROM playlists WHERE name=?", (playlist_name.strip().lower(),)).fetchone()
        sg = conn.execute("SELECT id FROM songs WHERE title=?", (song_title.strip(),)).fetchone()
        if pl and sg:
            conn.execute("INSERT OR IGNORE INTO playlist_songs VALUES (?,?)", (pl[0], sg[0]))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False

    @staticmethod
    def get_playlist_songs(playlist_name):
        conn = sqlite3.connect(DB_PATH)
        exists = conn.execute(
            "SELECT 1 FROM playlists WHERE name = ?",
            (playlist_name.strip().lower(),)
        ).fetchone()
        if not exists:
            conn.close()
            return None
        rows = conn.execute("""
            SELECT s.title, a.name
            FROM songs s
            JOIN playlist_songs ps ON s.id = ps.song_id
            JOIN playlists p ON p.id = ps.playlist_id
            JOIN artists a ON a.id = s.artist_id
            WHERE p.name = ?
        """, (playlist_name.strip().lower(),)).fetchall()
        conn.close()
        return [{"title": r[0], "artist": r[1]} for r in rows]

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    @staticmethod
    def analyze_input(text):
        keyword = ""
        genre = ""
        tempo = ""
        mood = ""

        tokens = re.split(r"[,\s]+", text.lower())

        for token in tokens:
            if token in SongLibrary.GENRES:
                genre = token
            elif token in SongLibrary.TEMPOS:
                tempo = token
            else:
                for standard, synonyms in SongLibrary.MOODS.items():
                    if token == standard or token in synonyms:
                        mood = standard
                        break
                else:
                    if token:
                        keyword = token

        return keyword, genre, tempo, mood

    @staticmethod
    def ranked_songs(keyword, genre, tempo, mood, song_list=None):
        if song_list is None:
            song_list = SongLibrary.load_songs()

        results = []
        for song in song_list:
            results.append((song.score(keyword, genre, tempo, mood), song))
        return sorted(results, key=lambda item: item[0], reverse=True)

