from app import db
from enum import Enum


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(32))
    type = db.Column(db.Integer)


class TournamentType(Enum):
    SINGLE = 1
    TWO_HEADED_GIANT = 2
