from src.helpers import db

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.String(255), primary_key=True)
    comment = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    rating_date = db.Column(db.String(50))
    song_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))

    def __init__(self, comment, rating, rating_date, song_id, user_id, id=None):
        self.id = id
        self.comment = comment
        self.rating = rating
        self.rating_date = rating_date
        self.song_id = song_id
        self.user_id = user_id
