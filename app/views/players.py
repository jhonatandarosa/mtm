from flask import Blueprint
from flask import render_template
from flask import request
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import not_
import functools

from app import Session
from app.model import Player
from app.model import Deck
from app.model import Game
from app.model import Participant

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


def to_sorted_list(data):
    rank = []

    for k in data.keys():
        v = data[k]
        v['id'] = k
        rank.append(v)

    def sort_f(a, b):
        ga = a['perc']
        gb = b['perc']

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
    deck_data = {}

    for game in games:
        if game.p1_wins == 0 and game.p2_wins == 0:
            continue

        is_p1_myself = id in pmap[game.p1_id]

        wins = 0
        losses = 0
        if is_p1_myself:
            my_team_decks = dmap[game.p1_id]
            my_team = pmap[game.p1_id]
            oponnets = pmap[game.p2_id]
            wins = game.p1_wins
            losses = game.p2_wins
        else:
            my_team_decks = dmap[game.p2_id]
            my_team = pmap[game.p2_id]
            oponnets = pmap[game.p1_id]
            wins = game.p2_wins
            losses = game.p1_wins

        for p in oponnets:
            if p is None:
                continue
            if p not in data:
                data[p] = {'w': 0, 'l': 0, 't': 0}

            data[p]['t'] += wins + losses
            data[p]['w'] += wins
            data[p]['l'] += losses

        if id == my_team[0]:
            my_deck = my_team_decks[0]
        else:
            my_deck = my_team_decks[1]

        if my_deck is not None:
            if my_deck not in deck_data:
                deck_data[my_deck] = {'w': 0, 'l': 0, 't': 0}

            deck_data[my_deck]['t'] += wins + losses
            deck_data[my_deck]['w'] += wins
            deck_data[my_deck]['l'] += losses

    for p in data:
        t = data[p]['t']
        w = data[p]['w']
        data[p]['perc'] = w / t * 100

    for p in deck_data:
        t = deck_data[p]['t']
        w = deck_data[p]['w']
        deck_data[p]['perc'] = w / t * 100

    return to_sorted_list(data), to_sorted_list(deck_data)


@bp.route('/')
def index_view():
    session = Session()
    players = session.query(Player).all()

    team = {}

    for player in players:
        name = player.name
        if player.nickname is not None:
            name = player.nickname

        team[player.id] = {
            'name': name
        }

    admin = request.args.get('admin', '') == 'True'

    ranking = Ranking()

    table = ranking.ranking_table(ranking.players, True)

    for id in team:
        player = team[id]
        player['link'] = '/players/%s' % id

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
    decks = session.query(Deck).all()

    pmap = {}
    for d in players:
        pmap[d.id] = d

    dmap = {}
    for d in decks:
        dmap[d.id] = d

    ranking = Ranking()
    rank_data = ranking.get_player_ranking(id)

    table = ranking.ranking_table([rank_data], True)

    games_data, decks_data = get_player_info(id)

    return render_template(
        'players/view_player.html',
        player=player,
        players=pmap,
        decks=dmap,
        ranking_table=table,
        games_data=games_data,
        decks_data=decks_data
    )


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
