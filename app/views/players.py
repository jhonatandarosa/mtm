from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Player

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


@bp.route('/')
def index_view():
    session = Session()
    players = session.query(Player).all()

    result = {}
    for player in players:
        result[player.id] = player

    admin = request.args.get('admin', '') == 'True'

    rank = Ranking().players

    return render_template('players/index.html', admin=admin, players=result, ranking=rank)
