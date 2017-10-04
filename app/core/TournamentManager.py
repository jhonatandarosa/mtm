from enum import Enum
import random
import itertools

from .SingletonDecorator import SingletonDecorator

from app import Session
from app.core import Ranking

from app.model import Deck
from app.model import Participant
from app.model import Tournament
from app.model import Game


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

    def new_tournament(self, tournament_type, name, players_ids):
        decks = self.get_available_decks_for_next_tournament()

        matches = self.match_decks_and_players(decks, players_ids)

        session = Session()

        tournament = Tournament()
        tournament.name = name
        tournament.status = 'active'
        tournament.type = tournament_type.value

        session.add(tournament)
        session.commit()

        participants = []
        if tournament_type == TournamentType.SINGLE:
            team = matches
            for match in matches:
                p = Participant()
                p.tournament_id = tournament.id
                p.player_id = match[0]
                p.deck_id = match[1]
                participants.append(p)
                session.add(p)

            rounds = list(itertools.combinations(participants, 2))

        elif tournament_type == TournamentType.TWO_HEADED_GIANT:
            teams = list(itertools.combinations(matches, 2))
            for team in teams:
                m1 = team[0]
                m2 = team[1]
                p = Participant()
                p.tournament_id = tournament.id
                p.player_id = m1[0]
                p.deck_id = m1[1]
                p.player2_id = m2[0]
                p.deck2_id = m2[1]
                participants.append(p)
                session.add(p)

            r = len(matches) - 1
            left = participants[:r]
            right = participants[::-1][:-r]
            rounds = []

            for i in range(0, len(left)):
                l = left[i]
                r = right[i]
                rounds.append((l, r))

        session.commit()

        # n = len(participants)
        # is_even = n % 2 == 0
        # rounds = n-1 if is_even else n

        # FIXME tournament with more than 4 players
        games = []
        for i, g in enumerate(rounds):
            game = Game()
            game.tournament_id = tournament.id
            game.p1_wins = 0
            game.p2_wins = 0
            game.round = i + 1
            game.p1_id = g[0].id
            game.p2_id = g[1].id

            games.append(game)
            session.add(game)

        session.commit()


TournamentManager = SingletonDecorator(TournamentManager)
