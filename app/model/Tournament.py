from app import db


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.String())


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    round = db.Column(db.Integer)
    p1_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p2_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p1_wins = db.Column(db.Integer)
    p2_wins = db.Column(db.Integer)
# from app import db
# from mongoalchemy import fields
#
#
# class Participant(db.Document):
#     player = fields.ObjectIdField()
#     deck = fields.ObjectIdField()
#
#
# class Game(db.Document):
#     p1 = fields.ObjectIdField()
#     p2 = fields.ObjectIdField()
#     result = fields.ListField(fields.IntField())
#
#
# class Round(db.Document):
#     id = fields.IntField()
#     games = fields.ListField(fields.DocumentField(Game))
#
#
# class Tournament(db.Document):
#     config_collection_name = 'tournaments'
#
#     name = fields.StringField()
#     participants = fields.ListField(fields.DocumentField(Participant))
#     rounds = fields.ListField(fields.DocumentField(Round))
