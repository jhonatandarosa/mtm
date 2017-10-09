from flask import Blueprint
from flask import render_template
from flask import request
from sqlalchemy import or_

from app import Session
from app.model import Player
from app.model import Game
from app.model import Participant

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


def get_player_info(id):
    session = Session()

    query = session \
        .query(
        Game,
        Participant.player_id,
        Participant.player2_id,
        Participant.deck_id,
        Participant.deck2_id
    ) \
        .join(Participant, or_(Game.p1_id == Participant.id, Game.p2_id == Participant.id)) \
        .filter(or_(Participant.player_id == id, Participant.player2_id == id))

    games = query.all()

    for game in games:
        pass

    participants = session.query(Participant).all()


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


@bp.route('/<int:id>')
def view_player(id):
    session = Session()

    player = session.query(Player).filter(Player.id == id).one()

    ranking = Ranking()
    rank_data = ranking.get_player_ranking(id)

    table = ranking.ranking_table([rank_data], True)

    get_player_info(id)

    return render_template(
        'players/view_player.html',
        player=player,
        ranking_table=table
    )
