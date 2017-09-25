from app import db


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(32))


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    __table_args__ = (
        db.UniqueConstraint('player_id', 'tournament_id', name='uix_player_tournament'),
        db.UniqueConstraint('deck_id', 'tournament_id', name='uix_deck_tournament')
    )


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
