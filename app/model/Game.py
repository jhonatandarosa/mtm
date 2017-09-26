from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    round = db.Column(db.Integer)
    p1_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p2_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    p1_wins = db.Column(db.Integer)
    p2_wins = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint('tournament_id', 'round', 'p1_id', name='uix_trp1'),
        db.UniqueConstraint('tournament_id', 'round', 'p2_id', name='uix_trp2')
    )
