from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Player
from app.model import Participant
from app.model import Tournament
from app.model import Game
from app.model import helper

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/tournaments', template_folder='templates/',
               static_folder='/static')


@bp.route('/')
def index_view():
    session = Session()
    tournaments = session.query(Tournament).order_by(Tournament.id.desc()).all()

    admin = request.args.get('admin', '') == 'True'

    return render_template('tournaments/index.html', admin=admin, tournaments=tournaments)


@bp.route('/<int:tid>')
def view_tournament(tid):
    session = Session()
    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()

    tournament = session.query(Tournament).filter(Tournament.id == tid).one()
    games = session.query(Game).filter(Game.tournament_id == tid).order_by(Game.id.asc()).all()
    players = session.query(Player).all()

    players_map = {}
    pmap = {}

    for player in players:
        players_map[player.id] = player

    for p in participants:
        pmap[p.id] = players_map[p.player_id]

    data = Ranking().get_tournament_ranking(tid)

    rounds = helper.group_by_round(games)

    return render_template(
        'tournaments/view_tournament.html',
        participants=pmap,
        players=players_map,
        tournament=tournament,
        rounds=rounds, data=data
    )
