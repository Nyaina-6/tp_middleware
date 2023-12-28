from src.helpers import db

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.String(255), primary_key=True)
    artist = db.Column(db.String(255))
    album = db.Column(db.String(255))
    title = db.Column(db.String(255))
    realease_year = db.Column(db.Integer)
    genre = db.Column(db.String(100))

    def __init__(self, song_id, artist, album, title, realease_year, genre):
        self.id = song_id
        self.artist = artist
        self.album = album
        self.title = title
        self.release_year = realease_year
        self.genre = genre

    def is_empty(self):
        return (not self.id or self.id == "") and \
               (not self.artist or self.artist == "") and \
               (not self.album or self.album == "") and \
               (not self.title or self.title == "") and \
               (not self.realease_year or self.realease_year == 0) and \
               (not self.genre or self.genre == "")
