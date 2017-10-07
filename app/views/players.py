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

    team = {}

    for player in players:
        team[player.id] = {
            'name': player.name
        }

    admin = request.args.get('admin', '') == 'True'

    ranking = Ranking()

    table = ranking.ranking_table(ranking.players, True)

    return render_template(
        'players/index.html',
        admin=admin,
        rank_table=table,
        teams=team
    )
