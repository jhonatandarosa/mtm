from app import db


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
