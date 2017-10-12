import functools

from app import Session
from app.model import Deck
from app.model import Game
from app.model import Participant
from app.model import Tournament
from app.model import TournamentType
from .SingletonDecorator import SingletonDecorator

sts = ['mw', 'ml', 'w', 'l', 'pts', 't', 'tp']


def create_stats():
    stats = {}
    for s in sts:
        stats[s] = 0
    return stats


def ranking_sort(a, b):
    ga = a['pts']
    gb = b['pts']
    return (gb > ga) - (gb < ga)


def ranking(data):
    rank = []

    for k in data.keys():
        d = dict(data[k])
        d['id'] = k
        rank.append(d)

    rank.sort(key=functools.cmp_to_key(ranking_sort))

    return rank


def thg_players_ranking(parts_players, data):
    rank_players = {}
    for k in data.keys():
        pids = parts_players[k]
        for id in pids:
            if id not in rank_players:
                rank_players[id] = create_stats()

            for s in sts:
                rank_players[id][s] += data[k][s]

    return ranking(rank_players)


def calc_points(wins, loses):
    pts = wins * 3

    if wins > loses and wins > 0:
        pts += 3

    played = wins > 0 or loses > 0
    drawn = wins == loses
    finished = wins == 2 or loses == 2

    if played and (drawn or not finished):
        pts += 1
    elif pts > 0 and loses > 0:
        pts -= 1

    return pts


def get_participants_stats(games):
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

            wins = entry[0][1]
            loses = entry[1][1]
            pts = calc_points(wins, loses)

            parts_stats[p]['w'] += wins
            parts_stats[p]['l'] += loses
            parts_stats[p]['pts'] += pts
            parts_stats[p]['mw'] += 1 if wins > loses else 0
            parts_stats[p]['ml'] += 1 if loses > wins else 0

    return parts_stats


def calculate_tournament_stats(items, attr, tournaments, ts_map, parts_rank):
    for item in items:

        for tid in tournaments:
            data = tournaments[tid]
            tournament = ts_map[tid]
            if tournament.status != 'finished':
                continue

            is_thg = tournament.type == TournamentType.TWO_HEADED_GIANT.value

            if is_thg:
                data = data[attr]
                # ids = (data[0]['id'], None)
                # ids = parts_rank[data[0]['id']]

            for i, d in enumerate(data):
                did = d['id']
                ids = (did, None) if is_thg else parts_rank[did]

                if item['id'] in ids:
                    item['tp'] += 1
                    if i == 0:
                        item['t'] += 1


class Ranking:
    players = []
    decks = []
    tournaments = []

    def refresh(self):
        session = Session()
        session.flush()
        games = session.query(Game).order_by(Game.id.asc()).all()
        decks = session.query(Deck).filter(Deck.id > 0).order_by(Deck.id.asc()).all()
        participants = session.query(Participant).all()

        ts = session.query(Tournament).all()

        ts_map = {}
        for t in ts:
            ts_map[t.id] = t

        parts_stats = get_participants_stats(games)

        parts_players = {}
        parts_decks = {}

        for p in participants:
            parts_players[p.id] = (p.player_id, p.player2_id)
            parts_decks[p.id] = (p.deck_id, p.deck2_id)

        players_stats = {}
        decks_stats = {}
        tournament_stats = {}

        for participant in participants:
            pid = participant.player_id
            did = participant.deck_id
            pid2 = participant.player2_id
            did2 = participant.deck2_id
            tid = participant.tournament_id

            if pid not in players_stats:
                players_stats[pid] = create_stats()

            if ts_map[tid].type != TournamentType.DRAFT.value:
                if did not in decks_stats:
                    decks_stats[did] = create_stats()

            if tid not in tournament_stats:
                tournament_stats[tid] = {}

            if participant.id not in tournament_stats[tid]:
                tournament_stats[tid][participant.id] = create_stats()

            for s in sts:
                if ts_map[tid].status == 'finished':
                    players_stats[pid][s] += parts_stats[participant.id][s]

                    if ts_map[tid].type != TournamentType.DRAFT.value:
                        decks_stats[did][s] += parts_stats[participant.id][s]

                    if ts_map[tid].type == TournamentType.TWO_HEADED_GIANT.value:
                        players_stats[pid2][s] += parts_stats[participant.id][s]
                        decks_stats[did2][s] += parts_stats[participant.id][s]

                tournament_stats[tid][participant.id][s] += parts_stats[participant.id][s]

        self.players = ranking(players_stats)
        self.decks = ranking(decks_stats)

        for deck in decks:
            if deck.id not in decks_stats:
                dstats = create_stats()
                dstats['id'] = deck.id
                self.decks.append(dstats)

        self.tournaments = {}
        for tid in tournament_stats:
            tournament = ts_map[tid]
            if tournament.type == TournamentType.TWO_HEADED_GIANT.value:
                self.tournaments[tid] = {
                    'players': thg_players_ranking(parts_players, tournament_stats[tid]),
                    'decks': thg_players_ranking(parts_decks, tournament_stats[tid]),
                    'teams': ranking(tournament_stats[tid])
                }
            else:
                self.tournaments[tid] = ranking(tournament_stats[tid])

        calculate_tournament_stats(self.players, 'players', self.tournaments, ts_map, parts_players)
        calculate_tournament_stats(self.decks, 'decks', self.tournaments, ts_map, parts_decks)

    def get_tournament_ranking(self, id):
        return self.tournaments[id]

    def get_player_ranking(self, id):
        for player in self.players:
            if player['id'] == id:
                return player
        return None

    def ranking_table(self, data, show_tournaments=False):
        table = {}
        table['headers'] = ['Name', 'M. Played', 'M. Won', 'M. Lost', 'G. Played', 'G. Won', 'G. Lost', 'Pts', '% Pts']
        table['cols'] = ['mp', 'mw', 'ml', 'p', 'w', 'l', 'pts', 'ppts']
        if show_tournaments:
            table['headers'].insert(1, 'T. Won')
            table['headers'].insert(1, 'T. Played')
            table['cols'].insert(0, 't')
            table['cols'].insert(0, 'tp')

        rows = []

        for rank in data:
            row = dict(rank)
            row['mp'] = row['mw'] + row['ml']
            row['p'] = row['w'] + row['l']
            if row['mp'] > 0:
                ppts = row['pts'] / (row['mp'] * 9) * 100
            else:
                ppts = 0
            row['ppts'] = "{0:.2f}".format(round(ppts, 2))
            rows.append(row)

        table['rows'] = rows
        return table


Ranking = SingletonDecorator(Ranking)
