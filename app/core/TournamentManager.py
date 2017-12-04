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


def group_by_key(data, key):
    groups = {}

    for d in data:
        kv = d[key]
        if kv not in groups:
            groups[kv] = []
        groups[kv].append(d)

    return groups


def sort_grouped_lists(grouped_lists, sort_fn):
    for group in grouped_lists:
        lst = grouped_lists[group]
        lst.sort(key=functools.cmp_to_key(sort_fn))


def randomize_grouped_by_matchs_played(decks, play_map):
    groups = []

    for deck in decks:
        mp = play_map[deck['id']]

        while len(groups) <= mp:
            groups.append([])

        groups[mp].append(deck)

    for group in groups:
        random.shuffle(group)

    return list(itertools.chain(*groups))


class TournamentManager:

    def get_winner_deck_id(self, tournament, participants, rank):
        if tournament.type == TournamentType.TWO_HEADED_GIANT.value:
            return rank['decks'][0]['id']
        else:
            pid = rank[0]['id']
            participant = participants[pid]
            return participant.deck_id


    def get_available_decks_for_next_tournament(self, tier):
        session = Session()

        ds = session.query(Deck).filter(Deck.status == 'active').all()
        parts = session.query(Participant).all()
        # tournaments = session.query(Tournament).filter(Tournament.status == 'finished').order_by(
        #     Tournament.id.asc()).all()

        decks = {}
        participants = {}

        for p in parts:
            participants[p.id] = p

        for deck in ds:
            decks[deck.id] = deck

        ranking = Ranking()
        # for tournament in tournaments:
        #     if tournament.type == TournamentType.DRAFT.value:
        #         continue
        #     t = ranking.get_tournament_ranking(tournament.id)
        #     winner = self.get_winner_deck_id(tournament, participants, t)
        #
        #     deck = decks[winner]
        #
        #     result.remove(deck)

        # sort decks
        play_map = {}
        for deck_data in ranking.decks:
            mp = deck_data['tp']

            play_map[deck_data['id']] = mp

        def deck_sort(a, b):
            ga = play_map[a['id']]
            gb = play_map[b['id']]

            return (ga > gb) - (ga < gb)

        tiers = group_by_key(ranking.decks, 'tier')

        sort_grouped_lists(tiers, deck_sort)

        for t in tiers:
            lst = tiers[t]
            tiers[t] = randomize_grouped_by_matchs_played(lst, play_map)

        if tier == 'T1':
            order = ['T1', 'T2', 'T3']
        elif tier == 'T2':
            order = ['T2', 'T3', 'T1']
        else:
            order = ['T3', 'T2', 'T1']

        result = []
        for t in order:
            lst = tiers[t]
            for d in lst:
                did = d['id']
                if did not in decks:
                    continue
                result.append(decks[did])

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

    def round_robin_schedule(self, participants, team=False):
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

            competitors = [left[0]] + [right[0]] + left[1:] + right[1:][::-1]

        def impossible_game(game):
            p1 = game['p1']
            p2 = game['p2']
            par1 = {p1.player_id, p1.player2_id}
            par2 = {p2.player_id, p2.player2_id}
            intersect = par1.intersection(par2)

            return len(intersect) > 0

        if team:
            schedule = [x for x in schedule if not impossible_game(x)]
            # fix rounds
            r = 0
            g = 0
            for game in schedule:
                game['round'] = r
                g += 1
                if g >= len(schedule) / rounds:
                    g = 0
                    r += 1

        for s in schedule:
            if team:
                print('%s (%s,%s)x(%s,%s)' % (s['round'], s['p1'].player_id, s['p1'].player2_id, s['p2'].player_id, s['p2'].player2_id))
            else:
                print('%s %sx%s' % (s['round'], s['p1'].player_id, s['p2'].player_id))

        return schedule

    def generate_schedule_single(self, matches):
        participants = []

        for match in matches:
            p = Participant()
            p.player_id = match[0]
            p.deck_id = match[1]
            participants.append(p)

        schedule = self.round_robin_schedule(participants)

        return schedule, participants

    def generate_schedule_draft(self, matches):
        participants = []

        for match in matches:
            p = Participant()
            p.player_id = match[0]
            # p.deck_id = match[1] # no decks
            participants.append(p)

        schedule = self.round_robin_schedule(participants)

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

        schedule = self.round_robin_schedule(participants, True)

        return schedule, participants

    def generate_schedule(self, tournament_type, matches):

        if tournament_type == TournamentType.SINGLE:
            return self.generate_schedule_single(matches)
        elif tournament_type == TournamentType.TWO_HEADED_GIANT:
            return self.generate_schedule_thg(matches)
        elif tournament_type == TournamentType.DRAFT:
            return self.generate_schedule_draft(matches)

    def new_tournament(self, tournament_type, name, players_ids, tier=None):
        decks = self.get_available_decks_for_next_tournament(tier)

        matches = self.match_decks_and_players(decks, players_ids)

        schedule, participants = self.generate_schedule(tournament_type, matches)

        session = Session()

        tournament = Tournament()
        tournament.name = name
        tournament.status = 'active'
        tournament.type = tournament_type.value

        session.add(tournament)
        session.commit()

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
