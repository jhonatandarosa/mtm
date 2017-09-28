import functools

from .SingletonDecorator import SingletonDecorator

from app import Session
from app.model import Player
from app.model import Game
from app.model import Participant

sts = ['mw', 'ml', 'w', 'l', 'pts']


def create_stats():
    stats = {}
    for s in sts:
        stats[s] = 0
    return stats


def ranking_sort(a, b):
    # match wins
    if a['mw'] != b['mw']:
        return -1 if a['mw'] > b['mw'] else 1
    else:
        # games points diff
        if a['pts'] != b['pts']:
            return -1 if a['pts'] > b['pts'] else 1

    return 0


def ranking(data):
    rank = []

    for k in data.keys():
        d = dict(data[k])
        d['id'] = k
        rank.append(d)

    rank.sort(key=functools.cmp_to_key(ranking_sort))

    return rank


class Ranking:
    players = []
    decks = []
    tournaments = []

    def refresh(self):
        session = Session()
        games = session.query(Game).all()

        parts_stats = {}

        for game in games:
            p1 = game.p1_id
            p1w = game.p1_wins
            p2 = game.p2_id
            p2w = game.p2_wins

            for entry in [((p1, p1w), (p2, p2w)), ((p2, p2w), (p1, p1w))]:
                p = entry[0][0]
                if p not in parts_stats:
                    parts_stats[p] = create_stats()

                pts = entry[0][1] - entry[1][1]

                parts_stats[p]['w'] += entry[0][1]
                parts_stats[p]['l'] += entry[1][1]
                parts_stats[p]['pts'] += pts
                parts_stats[p]['mw'] += 1 if pts > 0 else 0
                parts_stats[p]['ml'] += 1 if pts < 0 else 0

        participants = session.query(Participant).all()

        parts_players = {}
        parts_decks = {}

        for p in participants:
            parts_players[p.id] = p.player_id
            parts_decks[p.id] = p.deck_id

        players_stats = {}
        decks_stats = {}
        tournament_stats = {}

        for participant in participants:
            pid = participant.player_id
            did = participant.deck_id
            tid = participant.tournament_id

            if pid not in players_stats:
                players_stats[pid] = create_stats()

            if did not in decks_stats:
                decks_stats[did] = create_stats()

            if tid not in tournament_stats:
                tournament_stats[tid] = {}

            if participant.id not in tournament_stats[tid]:
                tournament_stats[tid][participant.id] = create_stats()

            for s in sts:
                players_stats[pid][s] += parts_stats[participant.id][s]
                decks_stats[did][s] += parts_stats[participant.id][s]
                tournament_stats[tid][participant.id][s] += parts_stats[participant.id][s]

        self.players = ranking(players_stats)
        self.decks = ranking(decks_stats)

        self.tournaments = []
        for tid in tournament_stats:
            self.tournaments.append(ranking(tournament_stats[tid]))

        for player in self.players:
            player['t'] = 0

            for t in self.tournaments:
                pid = parts_players[t[0]['id']]
                if player['id'] == pid:
                    player['t'] += 1

        for deck in self.decks:
            deck['t'] = 0

            for t in self.tournaments:
                did = parts_decks[t[0]['id']]
                if deck['id'] == did:
                    deck['t'] += 1

    def get_tournament_ranking(self, id):
        return self.tournaments[id-1]


Ranking = SingletonDecorator(Ranking)
