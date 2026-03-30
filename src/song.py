class Song:
    def __init__(self, title, keywords, genre, tempo, mood):
        self.title = title
        self.keywords = keywords
        self.genre = genre
        self.tempo = tempo
        self.mood = mood

    def score(self, keyword, genre, tempo, mood):
        score = 0
        if keyword and keyword in self.keywords:
            score += 2
        if genre and self.genre == genre:
            score += 1
        if tempo and self.tempo == tempo:
            score += 1
        if mood and self.mood == mood:
            score += 1
        return score