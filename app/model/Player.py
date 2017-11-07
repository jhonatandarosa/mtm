from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    nickname = db.Column(db.String(64))
