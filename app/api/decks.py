from flask import Blueprint
from flask import request

from app import Session
from app.model import Deck
from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__)


@bp.route('/api/decks', methods=['POST'])
def create_deck():
    payload = request.json
    if 'name' not in payload or len(payload['name'].strip()) == 0:
        return None, 400

    deck = Deck()
    deck.name = payload['name']
    deck.type = 1
    deck.status = 'active'

    session = Session()
    session.add(deck)
    session.commit()

    Ranking().refresh()

    return '', 200


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
