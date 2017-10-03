from flask import Blueprint
from flask import request
from flask import make_response
from flask import abort

from app import Session
from app.model import Game
from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__)


@bp.route('/api/tournaments', methods=['POST'])
def new_tournament():
    payload = request.json
    params = ['name', 'type', 'players']
    for param in params:
        if param not in payload:
            abort(400)

    name = payload['name']
    type = payload['type']
    players = payload['players']

    Ranking().refresh()

    return make_response()
