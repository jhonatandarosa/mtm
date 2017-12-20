import functools

from app import Session
from app.model import Deck
from app.model import Game
from app.model import Participant
from app.model import Tournament
from app.model import TournamentType
from .SingletonDecorator import SingletonDecorator

from sqlalchemy import or_, and_

sts = ['mp', 'mw', 'ml', 'p', 'w', 'l', 'pts', 't', 'tp']


def create_stats():
    stats = {}
    for s in sts:
        stats[s] = 0
    return stats


def get_tier(deck):
    if deck['mp'] > 0:
        ppts = deck['pts'] / (deck['mp'] * 9) * 100
    else:
        ppts = 0

    if ppts > 70:
        return 'T1'
    elif ppts > 35:
        return 'T2'
    else:
        return 'T3'


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


def tie_breaker(rank):
    p1 = rank[0]
    p2 = rank[1]

    p1_wins = 0
    p2_wins = 0
    if p1['pts'] == p2['pts']:
        session = Session()
        games = session.query(Game) \
            .filter(
            or_(
                and_(Game.p1_id == p1['id'], Game.p2_id == p2['id']),
                and_(Game.p1_id == p2['id'], Game.p2_id == p1['id'])
            )
        ) \
            .order_by(Game.id.asc()) \
            .all()

        for game in games:
            if game.p1_id == p1['id']:
                if game.p1_wins > game.p2_wins:
                    p1_wins += 1
                else:
                    p2_wins += 1
            else:
                if game.p1_wins > game.p2_wins:
                    p2_wins += 1
                else:
                    p1_wins += 1

        if p2_wins > p1_wins:
            rank[0] = p2
            rank[1] = p1

    return rank


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

            parts_stats[p]['mp'] += max(0, min(wins + loses, 1))
            parts_stats[p]['w'] += wins
            parts_stats[p]['l'] += loses
            parts_stats[p]['p'] += wins + loses
            parts_stats[p]['pts'] += pts
            parts_stats[p]['mw'] += 1 if wins > loses else 0
            parts_stats[p]['ml'] += 1 if loses > wins else 0

    return parts_stats


def calculate_tournament_stats(items, attr, tournaments, ts_map, parts_rank, ttype=None):
    for item in items:

        for tid in tournaments:
            data = tournaments[tid]
            tournament = ts_map[tid]
            if ttype is not None and ttype != tournament.type:
                continue
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


def get_title(ttype):
    if ttype == TournamentType.SINGLE.value:
        return 'DGT Master'
    elif ttype == TournamentType.TWO_HEADED_GIANT.value:
        return 'Giant Master'
    elif ttype == TournamentType.DRAFT.value:
        return 'Draft Master'
    return None


class Ranking:

    def __init__(self, year) -> None:
        super().__init__()
        self.year = year
        self.players = []
        self.decks = []
        self.tournaments = []
        self.tournaments_types = {}
        self.titles = {}

    def refresh(self):
        self.players = []
        self.decks = []
        self.tournaments = []
        self.tournaments_types = {}
        self.titles = {}
        almost_there_count = {}

        session = Session()
        session.flush()

        decks = session.query(Deck).filter(Deck.id > 0).order_by(Deck.id.asc()).all()

        if self.year is not None:
            ts = session.query(Tournament).filter(Tournament.year == self.year).all()

            participants = session.query(Participant) \
                .join(Tournament, Participant.tournament_id == Tournament.id) \
                .filter(Tournament.year == self.year).all()

            games = session.query(Game) \
                .join(Tournament, Game.tournament_id == Tournament.id) \
                .filter(Tournament.year == self.year) \
                .order_by(Game.id.asc()).all()

        else:
            ts = session.query(Tournament).all()
            participants = session.query(Participant).all()
            games = session.query(Game).order_by(Game.id.asc()).all()

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
        tournaments_types_stats = {}

        types = [TournamentType.SINGLE.value, TournamentType.TWO_HEADED_GIANT.value, TournamentType.DRAFT.value]
        for ttype in types:
            tournaments_types_stats[ttype] = {}

        for participant in participants:
            pid = participant.player_id
            did = participant.deck_id
            pid2 = participant.player2_id
            did2 = participant.deck2_id
            tid = participant.tournament_id

            if pid not in players_stats:
                players_stats[pid] = create_stats()
                for type in types:
                    tournaments_types_stats[type][pid] = create_stats()

            if pid2 is not None and pid2 not in players_stats:
                players_stats[pid2] = create_stats()
                for type in types:
                    tournaments_types_stats[type][pid2] = create_stats()

            if ts_map[tid].type != TournamentType.DRAFT.value:
                if did not in decks_stats:
                    decks_stats[did] = create_stats()

                if did2 is not None and did2 not in decks_stats:
                    decks_stats[did2] = create_stats()

            if tid not in tournament_stats:
                tournament_stats[tid] = {}

            if participant.id not in tournament_stats[tid]:
                tournament_stats[tid][participant.id] = create_stats()

            for s in sts:
                if ts_map[tid].status == 'finished':
                    ttype = ts_map[tid].type
                    players_stats[pid][s] += parts_stats[participant.id][s]
                    tournaments_types_stats[ttype][pid][s] += parts_stats[participant.id][s]

                    if ttype != TournamentType.DRAFT.value:
                        decks_stats[did][s] += parts_stats[participant.id][s]

                    if ttype == TournamentType.TWO_HEADED_GIANT.value:
                        players_stats[pid2][s] += parts_stats[participant.id][s]
                        decks_stats[did2][s] += parts_stats[participant.id][s]
                        tournaments_types_stats[ttype][pid2][s] += parts_stats[participant.id][s]

                tournament_stats[tid][participant.id][s] += parts_stats[participant.id][s]

        self.players = ranking(players_stats)
        self.decks = ranking(decks_stats)

        for deck in decks:
            if deck.id not in decks_stats:
                dstats = create_stats()
                dstats['id'] = deck.id
                self.decks.append(dstats)

        for deck in self.decks:
            deck['tier'] = get_tier(deck)

        self.tournaments = {}
        for tid in tournament_stats:
            tournament = ts_map[tid]
            if tournament.type == TournamentType.TWO_HEADED_GIANT.value:
                self.tournaments[tid] = {
                    'players': thg_players_ranking(parts_players, tournament_stats[tid]),
                    'decks': thg_players_ranking(parts_decks, tournament_stats[tid]),
                    'teams': ranking(tournament_stats[tid])
                }
                prank = self.tournaments[tid]['players']
            else:
                trank = ranking(tournament_stats[tid])
                trank = tie_breaker(trank)
                prank = trank
                self.tournaments[tid] = trank
            if tournament.status == 'finished':
                second_in_line = prank[1]
                if tournament.type == TournamentType.TWO_HEADED_GIANT.value:
                    prank_pid = second_in_line['id']
                else:
                    prank_pid = parts_players[second_in_line['id']][0]
                if prank_pid not in almost_there_count:
                    almost_there_count[prank_pid] = 0
                almost_there_count[prank_pid] += 1

        calculate_tournament_stats(self.players, 'players', self.tournaments, ts_map, parts_players)
        calculate_tournament_stats(self.decks, 'decks', self.tournaments, ts_map, parts_decks)

        for ttype in tournaments_types_stats:
            stats = tournaments_types_stats[ttype]
            if len(stats) == 0:
                continue
            stats = ranking(stats)
            calculate_tournament_stats(stats, 'players', self.tournaments, ts_map, parts_players, ttype)
            self.tournaments_types[ttype] = stats
            pid = stats[0]['id']
            if pid not in self.titles:
                self.titles[pid] = []
            self.titles[pid].append(get_title(ttype))
            if len(self.titles[pid]) == 3:
                self.titles[pid] = ['MTG Master']

        almost_there_max = 0
        for pid in almost_there_count:
            if almost_there_count[pid] > almost_there_max:
                almost_there_max = almost_there_count[pid]

        for pid in almost_there_count:
            if almost_there_count[pid] == almost_there_max:
                if pid not in self.titles:
                    self.titles[pid] = []
                self.titles[pid].append('Quase lá')

    def get_tournament_ranking(self, id):
        return self.tournaments[id]

    def contains_tournament(self, id):
        return id in self.tournaments

    def get_player_ranking(self, id):
        for player in self.players:
            if player['id'] == id:
                return player
        return None
