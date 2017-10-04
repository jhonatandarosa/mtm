from app import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    deck2_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    __table_args__ = (
        db.UniqueConstraint('player_id', 'tournament_id', name='uix_player_tournament'),
        db.UniqueConstraint('player2_id', 'tournament_id', name='uix_player2_tournament'),
        db.UniqueConstraint('deck_id', 'tournament_id', name='uix_deck_tournament'),
        db.UniqueConstraint('deck2_id', 'tournament_id', name='uix_deck2_tournament'),
        db.CheckConstraint('player_id <> player2_id', name='ck_players'),
        db.CheckConstraint('deck_id <> deck2_id', name='ck_decks')
    )
