from flask import Blueprint
from flask import request
from flask import make_response
from flask import abort

from app import Session
from app.model import Game
from app.model import Tournament
from app.model import TournamentType
from app.core import RankingManager
from app.core import TournamentManager

bp = Blueprint('blueprint_%s' % __name__, __name__)


@bp.route('/api/tournaments', methods=['POST'])
def new_tournament():
    payload = request.json
    params = ['name', 'type', 'players', 'tier']
    for param in params:
        if param not in payload:
            abort(400)

    name = payload['name']
    type = payload['type']
    players = payload['players']
    tier = payload['tier']

    if name.strip() == '':
        abort(400)

    if tier.strip() == '':
        abort(400)

    if tier not in ['T1', 'T2', 'T3']:
        abort(400)

    if len(players) < 4:
        abort(400)

    ttype = TournamentType(type)

    if ttype is None:
        abort(400)

    manager = TournamentManager()
    manager.new_tournament(ttype, name, players, tier)

    RankingManager().refresh()

    return make_response()


@bp.route('/api/tournaments/<int:tid>/status', methods=['PUT'])
def change_status(tid):
    payload = request.json
    params = ['status']
    for param in params:
        if param not in payload:
            abort(400)

    status = payload['status']

    session = Session()

    tournament = session.query(Tournament).filter(Tournament.id == tid).one()
    if status == 'finished':
        tournament.status = 'finished'
        session.add(tournament)
        session.commit()

    RankingManager().refresh()

    return make_response()


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
