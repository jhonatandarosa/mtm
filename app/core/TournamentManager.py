from enum import Enum
import random
import itertools

from .SingletonDecorator import SingletonDecorator

from app import Session
from app.core import Ranking

from app.model import Deck
from app.model import Participant
from app.model import Tournament


class TournamentType(Enum):
    SINGLE = 1
    TWO_HEADED_GIANT = 2


class TournamentManager:

    def get_winner(self, rank):
        return rank[0]['id']

    def get_available_decks_for_next_tournament(self):
        session = Session()

        ds = session.query(Deck).all()
        parts = session.query(Participant).all()

        decks = {}
        participants = {}

        for p in parts:
            participants[p.id] = p

        result = []
        for deck in ds:
            decks[deck.id] = deck
            result.append(deck)

        for tid in Ranking().tournaments:
            t = Ranking().get_tournament_ranking(tid)
            winner = self.get_winner(t)

            participant = participants[winner]
            deck = decks[participant.deck_id]

            result.remove(deck)

        return result

    def get_last_decks_from_player(self, player):
        d = []

        session = Session()
        parts = session.query(Participant) \
            .filter(Participant.player_id == player) \
            .order_by(Participant.id.desc()) \
            .limit(2) \
            .all()

        for p in parts:
            d.append(p.deck_id)

        return d

    def match_decks_and_players(self, decks, players):
        random.shuffle(decks)

        matches = []

        for player in players:
            last_decks = self.get_last_decks_from_player(player)

            possible_decks = [d for d in decks if d.id not in last_decks]

            random.shuffle(possible_decks)
            deck = possible_decks[0]
            decks.remove(deck)

            matches.append((player, deck.id))

        return matches

    def new_tournament(self, tournament_type, **kwargs):
        decks = self.get_available_decks_for_next_tournament()

        players = [1, 2, 3, 4]

        matches = self.match_decks_and_players(decks, players)

        tournament = Tournament()
        # tournament.type = tournament_type.value

        participants = []
        if tournament_type == TournamentType.SINGLE:

            for match in matches:
                p = Participant()
                p.tournament_id = tournament.id
                p.player_id = match[0]
                p.deck_id = match[1]
                participants.append(p)

        elif tournament_type == TournamentType.TWO_HEADED_GIANT:
            pairs = list(itertools.combinations(matches, 2))
            for pair in pairs:
                m1 = pair[0]
                m2 = pair[1]
                p = Participant()
                p.tournament_id = tournament.id
                p.player_id = m1[0]
                p.deck_id = m1[1]
                # p.player2_id = m2[0]
                # p.deck2_id = m2[1]
                participants.append(p)

        pairs = list(itertools.combinations(participants, 2))

        games = []

    def test(self):
        self.new_tournament(TournamentType.TWO_HEADED_GIANT)


TournamentManager = SingletonDecorator(TournamentManager)
