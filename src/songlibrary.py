import re
from .song import Song


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
    songs = [
        Song("Blinding Lights", ["night", "city", "love"], "pop", "fast", "happy"),
        Song("Someone Like You", ["love", "heartbreak"], "pop", "slow", "sad"),
        Song("Lose Yourself", ["motivation", "dream", "fight"], "hiphop", "fast", "energetic"),
        Song("We Will Rock You", ["motivation", "power", "stadium"], "rock", "medium", "energetic"),
        Song("Gasolina", ["party", "dance"], "latin", "fast", "energetic"),
        Song("Clair de Lune", ["calm", "night", "piano"], "classical", "slow", "peaceful"),
        Song("Levels", ["party", "energy", "festival"], "edm", "fast", "energetic"),
        Song("Take Five", ["jazz", "relax", "night"], "jazz", "medium", "cool"),
        Song("No Woman No Cry", ["life", "hope", "freedom"], "reggae", "slow", "warm"),
        Song("The Hills", ["dark", "night", "love"], "rnb", "medium", "moody"),
        Song("Fear of the Dark", ["dark", "fear", "night"], "metal", "fast", "aggressive"),
        Song("River", ["soul", "emotion", "heartbreak"], "soul", "slow", "emotional"),
        Song("Shape of You", ["love", "dance", "night"], "pop", "medium", "romantic"),
        Song("Smells Like Teen Spirit", ["rebellion", "youth"], "rock", "fast", "angry"),
        Song("Blue World", ["chill", "vibes", "thinking"], "lofi", "slow", "relaxed"),
    ]

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
            song_list = SongLibrary.songs

        results = []
        for song in song_list:
            results.append((song.score(keyword, genre, tempo, mood), song))
        return sorted(results, key=lambda item: item[0], reverse=True)
