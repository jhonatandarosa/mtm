import functools
import itertools
import random

from sqlalchemy import or_

from app import Session
from app.core import Ranking
from app.model import Deck
from app.model import Game
from app.model import Participant
from app.model import Tournament
from app.model import TournamentType
from .SingletonDecorator import SingletonDecorator


class TournamentManager:

    def get_winner_deck_id(self, tournament, participants, rank):
        if tournament.type == TournamentType.TWO_HEADED_GIANT.value:
            return rank['decks'][0]['id']
        else:
            pid = rank[0]['id']
            participant = participants[pid]
            return participant.deck_id


    def get_available_decks_for_next_tournament(self):
        session = Session()

        ds = session.query(Deck).filter(Deck.status == 'active').all()
        parts = session.query(Participant).all()
        tournaments = session.query(Tournament).filter(Tournament.status == 'finished').order_by(
            Tournament.id.asc()).all()

        decks = {}
        participants = {}

        for p in parts:
            participants[p.id] = p

        result = []
        for deck in ds:
            decks[deck.id] = deck
            result.append(deck)

        ranking = Ranking()
        for tournament in tournaments:
            t = ranking.get_tournament_ranking(tournament.id)
            winner = self.get_winner_deck_id(tournament, participants, t)

            deck = decks[winner]

            result.remove(deck)

        # sort decks
        play_map = {}
        for deck_data in ranking.decks:
            w = deck_data['w']
            l = deck_data['l']

            play_map[deck_data['id']] = w + l

        def deck_sort(a, b):
            ga = play_map[a.id]
            gb = play_map[b.id]

            return (ga > gb) - (ga < gb)

        result.sort(key=functools.cmp_to_key(deck_sort))
        return result

    def get_last_decks_from_player(self, player):
        d = []

        session = Session()
        query = session.query(Participant) \
            .filter(or_(Participant.player_id == player, Participant.player2_id == player)) \
            .order_by(Participant.id.desc())

        for p in query:
            id = p.deck_id if p.player_id == player else p.deck2_id

            if id not in d:
                d.append(id)
            if len(d) == 2:
                break

        return d

    def match_decks_and_players(self, decks, players):
        random.shuffle(players)

        matches = []

        for player in players:
            last_decks = self.get_last_decks_from_player(player)

            possible_decks = [d for d in decks if d.id not in last_decks]

            deck = possible_decks[0]
            decks.remove(deck)

            matches.append((player, deck.id))

        return matches

    def generate_schedule_single(self, matches):
        participants = []

        for match in matches:
            p = Participant()
            p.player_id = match[0]
            p.deck_id = match[1]
            participants.append(p)

        n = len(participants)
        is_even = n % 2 == 0
        is_odd = not is_even
        rounds = n - 1 if is_even else n
        games_count = int(n / 2 * (n - 1))

        competitors = []
        competitors.extend(participants)
        if is_odd:
            competitors.append(None)

        games_per_round = int(len(competitors) / 2)

        schedule = []

        for r in range(0, rounds):
            left = competitors[:games_per_round]
            right = competitors[::-1][:games_per_round]

            pairs = zip(left, right)
            ss = [{'round': r, 'p1': pair[0], 'p2': pair[1]} for pair in pairs if
                  pair[0] is not None and pair[1] is not None]
            schedule.extend(ss)

            competitors = [left[0]] + [right[0]] + left[1:] + right[1:]

        return schedule, participants

    def generate_schedule_draft(self, matches):
        participants = []

        for match in matches:
            p = Participant()
            p.player_id = match[0]
            # p.deck_id = match[1] # no decks
            participants.append(p)

        n = len(participants)
        is_even = n % 2 == 0
        is_odd = not is_even
        rounds = n - 1 if is_even else n
        games_count = int(n / 2 * (n - 1))

        competitors = []
        competitors.extend(participants)
        if is_odd:
            competitors.append(None)

        games_per_round = int(len(competitors) / 2)

        schedule = []

        for r in range(0, rounds):
            left = competitors[:games_per_round]
            right = competitors[::-1][:games_per_round]

            pairs = zip(left, right)
            ss = [{'round': r, 'p1': pair[0], 'p2': pair[1]} for pair in pairs if
                  pair[0] is not None and pair[1] is not None]
            schedule.extend(ss)

            competitors = [left[0]] + [right[0]] + left[1:] + right[1:]

        return schedule, participants

    def generate_schedule_thg(self, matches):
        participants = []
        teams = list(itertools.combinations(matches, 2))
        for team in teams:
            m1 = team[0]
            m2 = team[1]
            p = Participant()
            p.player_id = m1[0]
            p.deck_id = m1[1]
            p.player2_id = m2[0]
            p.deck2_id = m2[1]
            participants.append(p)

        r = len(matches) - 1
        left = participants[:r]
        right = participants[::-1][:-r]
        schedule = []

        for i in range(0, len(left)):
            l = left[i]
            r = right[i]
            schedule.append({
                'round': i + 1,
                'p1': l,
                'p2': r
            })

        return schedule, participants

    def generate_schedule(self, tournament_type, matches):

        if tournament_type == TournamentType.SINGLE:
            return self.generate_schedule_single(matches)
        elif tournament_type == TournamentType.TWO_HEADED_GIANT:
            return self.generate_schedule_thg(matches)
        elif tournament_type == TournamentType.DRAFT:
            return self.generate_schedule_draft(matches)

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

        schedule, participants = self.generate_schedule(tournament_type, matches)

        for participant in participants:
            participant.tournament_id = tournament.id
            session.add(participant)

        session.commit()

        for s in schedule:
            game = Game()
            game.tournament_id = tournament.id
            game.p1_wins = 0
            game.p2_wins = 0
            game.round = s['round']
            game.p1_id = s['p1'].id
            game.p2_id = s['p2'].id
            session.add(game)

            session.commit()


TournamentManager = SingletonDecorator(TournamentManager)
