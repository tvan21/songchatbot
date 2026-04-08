class Song:
    def __init__(self, title, keywords, genre, tempo, mood, artist=""):
        self.title = title
        self.artist = artist
        self.keywords = keywords
        self.genre = genre
        self.tempo = tempo
        self.mood = mood

    def score(self, keyword, genre, tempo, mood):
        score = 0
        kw_list = [k.strip().lower() for k in self.keywords]
        if keyword and keyword.strip().lower() in kw_list:
            score += 2
        if genre and self.genre.strip().lower() == genre.strip().lower():
            score += 1
        if tempo and self.tempo.strip().lower() == tempo.strip().lower():
            score += 1
        if mood and self.mood.strip().lower() == mood.strip().lower():
            score += 1
        return score