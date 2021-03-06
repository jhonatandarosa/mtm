from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Deck

from app.core import RankingManager

import functools

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/decks', template_folder='templates/',
               static_folder='/static')


def get_tier_class(tier):
    if tier == 'T1':
        return 'amber lighten-4'
    elif tier == 'T2':
        return 'grey lighten-4'
    else:
        return 'deep-orange lighten-4'


def tier_sort(rank):

    def _tier_sort(a, b):
        ga = a['pts'] / (a['mp'] * 9) * 100 if a['mp'] > 0 else 0
        gb = b['pts'] / (b['mp'] * 9) * 100 if b['mp'] > 0 else 0

        return (gb > ga) - (gb < ga)

    rank.sort(key=functools.cmp_to_key(_tier_sort))

    return rank


@bp.route('/')
def index_view():
    session = Session()
    decks = session.query(Deck).all()

    team = {}

    for deck in decks:
        _class = ''
        if deck.status == 'inactive':
            _class = 'blue-grey lighten-5'
        team[deck.id] = {
            'name': deck.name,
            '_class': _class
        }

    admin = request.args.get('admin', '') == 'True'

    rank_manager = RankingManager()
    ranking = rank_manager.get_ranking()

    table = rank_manager.ranking_table(ranking.decks, True)

    return render_template(
        'decks/index.html',
        admin=admin,
        rank_table=table,
        teams=team
    )


@bp.route('/tier')
def tier_view():
    session = Session()
    decks = session.query(Deck).all()

    team = {}

    for deck in decks:
        _class = ''
        if deck.status == 'inactive':
            _class = 'blue-grey lighten-5'
        team[deck.id] = {
            'name': deck.name,
            '_class': _class,
            'status': deck.status
        }

    admin = request.args.get('admin', '') == 'True'

    rank_manager = RankingManager()
    ranking = rank_manager.get_ranking()

    tiers = tier_sort(ranking.decks[:])

    tiers = [x for x in tiers if team[x['id']]['status'] != 'inactive']

    for deck in ranking.decks:
        data = team[deck['id']]

        if data['_class'] == '':
            data['_class'] = get_tier_class(deck['tier'])

    table = rank_manager.ranking_table(tiers, True)

    return render_template(
        'decks/index.html',
        admin=admin,
        rank_table=table,
        teams=team
    )


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
