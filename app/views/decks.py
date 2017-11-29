from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Deck

from app.core import Ranking

import functools

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/decks', template_folder='templates/',
               static_folder='/static')


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

    ranking = Ranking()

    table = ranking.ranking_table(ranking.decks, True)

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
            '_class': _class
        }

    admin = request.args.get('admin', '') == 'True'

    ranking = Ranking()

    tiers = tier_sort(ranking.decks)

    table = ranking.ranking_table(tiers, True)

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
