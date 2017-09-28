from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Player
from app.model import Participant

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


@bp.route('/')
def index_view():
    session = Session()
    players = session.query(Player).all()
    participants = session.query(Participant).filter().all()

    players_map = {}
    pmap = {}

    for player in players:
        players_map[player.id] = player

    for p in participants:
        pmap[p.id] = players_map[p.player_id]

    admin = request.args.get('admin', '') == 'True'

    rank = Ranking().players

    return render_template(
        'players/index.html',
        admin=admin,
        players=players_map,
        participants=pmap,
        ranking=rank
    )
