from flask import Blueprint
from flask import render_template
from flask import request
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import not_
import functools

from app import Session
from app.model import Player
from app.model import Game
from app.model import Participant

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


def to_sorted_list(data):
    rank = []

    for k in data.keys():
        v = data[k]
        rank.append({'id': k, 'value': v})

    def sort_f(a, b):
        ga = a['value']
        gb = b['value']

        return (gb > ga) - (gb < ga)

    rank.sort(key=functools.cmp_to_key(sort_f))

    return rank


def get_player_info(id):
    session = Session()

    query = session \
        .query(Game) \
        .join(Participant, or_(Game.p1_id == Participant.id, Game.p2_id == Participant.id)) \
        .filter(or_(Participant.player_id == id, Participant.player2_id == id)) \
        .filter(not_(and_(Game.p1_wins == 0, Game.p2_wins == 0)))

    games = query.all()
    participants = session.query(Participant).all()

    pmap = {}
    dmap = {}
    for p in participants:
        pmap[p.id] = (p.player_id, p.player2_id)
        dmap[p.id] = (p.deck_id, p.deck2_id)

    data = {}

    for game in games:
        if game.p1_wins == 0 and game.p2_wins == 0:
            continue

        is_p1_winner = game.p1_wins > game.p2_wins
        is_p1_myself = id in pmap[game.p1_id]

        if is_p1_myself:
            players = pmap[game.p2_id]
            if is_p1_winner:
                var = 'w'
            else:
                var = 'l'
        else:
            players = pmap[game.p1_id]
            if is_p1_winner:
                var = 'l'
            else:
                var = 'w'

        for p in players:
            if p not in data:
                data[p] = {'w': 0, 'l': 0, 't': 0}

            data[p]['t'] += 1
            data[p][var] += 1

    del data[None]

    mw_p = {}
    ml_p = {}

    for p in data:
        t = data[p]['t']
        w = data[p]['w']
        l = data[p]['l']

        mw_p[p] = w/t * 100
        ml_p[p] = l/t * 100

    return to_sorted_list(mw_p), to_sorted_list(ml_p)


@bp.route('/')
def index_view():
    session = Session()
    players = session.query(Player).all()

    team = {}

    for player in players:
        team[player.id] = {
            'name': player.name
        }

    admin = request.args.get('admin', '') == 'True'

    ranking = Ranking()

    table = ranking.ranking_table(ranking.players, True)

    return render_template(
        'players/index.html',
        admin=admin,
        rank_table=table,
        teams=team
    )


@bp.route('/<int:id>')
def view_player(id):
    session = Session()

    player = session.query(Player).filter(Player.id == id).one()
    players = session.query(Player).all()

    pmap = {}
    for p in players:
        pmap[p.id] = p

    ranking = Ranking()
    rank_data = ranking.get_player_ranking(id)

    table = ranking.ranking_table([rank_data], True)

    mw_p, ml_p, = get_player_info(id)

    return render_template(
        'players/view_player.html',
        player=player,
        players=pmap,
        ranking_table=table,
        mw_p=mw_p,
        ml_p=ml_p,
    )


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
