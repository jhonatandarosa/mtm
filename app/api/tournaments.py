from flask import Blueprint
from flask import request
from flask import make_response
from flask import abort

from app import Session
from app.model import Game
from app.model import Tournament
from app.core import Ranking
from app.core import TournamentType
from app.core import TournamentManager

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

    if name.strip() == '':
        abort(400)

    if len(players) < 4:
        abort(400)

    ttype = None
    if type == TournamentType.SINGLE.value:
        ttype = TournamentType.SINGLE
    elif type == TournamentType.TWO_HEADED_GIANT.value:
        ttype = TournamentType.TWO_HEADED_GIANT

    if ttype is None:
        abort(400)

    manager = TournamentManager()
    manager.new_tournament(ttype, name, players)

    Ranking().refresh()

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

    Ranking().refresh()

    return make_response()
