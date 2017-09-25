from flask import Blueprint
from flask import request
from flask import make_response

from app import Session
from app.model import Player

bp = Blueprint('blueprint_%s' % __name__, __name__)


@bp.route('/api/players', methods=['POST'])
def create_player():
    payload = request.json
    if 'name' not in payload or len(payload['name'].strip()) == 0:
        return None, 400

    player = Player()
    player.name = payload['name']

    session = Session()
    session.add(player)
    session.commit()

    return '', 200
