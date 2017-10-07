from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Deck

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/decks', template_folder='templates/',
               static_folder='/static')


@bp.route('/')
def index_view():
    session = Session()
    decks = session.query(Deck).all()

    team = {}

    for deck in decks:
        _class = ''
        if deck.status == 'inactive':
            _class = 'red lighten-5'
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
