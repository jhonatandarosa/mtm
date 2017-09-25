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

    result = {}
    for deck in decks:
        result[deck.id] = deck

    admin = request.args.get('admin', '') == 'True'

    rank = Ranking().decks

    return render_template('decks/index.html', admin=admin, players=result, ranking=rank)
