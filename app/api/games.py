from flask import Blueprint
from flask import request
from flask import make_response
from flask import abort

from app import Session
from app.model import Game
from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__)


@bp.route('/api/games/<int:gameId>', methods=['PUT'])
def update_game(gameId):
    payload = request.json
    params = ['p1Wins', 'p2Wins']
    for param in params:
        if param not in payload:
            abort(400)

    p1_wins = payload['p1Wins']
    p2_wins = payload['p2Wins']

    if not 0 <= p1_wins <= 2:
        abort(400)

    if not 0 <= p2_wins <= 2:
        abort(400)

    session = Session()
    game = session.query(Game).filter(Game.id == gameId).one()
    game.p1_wins = p1_wins
    game.p2_wins = p2_wins
    session.add(game)
    session.commit()

    Ranking().refresh()

    return make_response()


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
