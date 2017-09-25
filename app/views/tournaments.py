from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Player
from app.model import Participant
from app.model import Tournament
from app.model import Game

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/tournaments', template_folder='templates/',
               static_folder='/static')


def groupByRound(games):
    rounds = {}

    for game in games:
        if game.round not in rounds:
            rounds[game.round] = []

        rounds[game.round].append(game)

    result = []
    for r in rounds:
        result.append(rounds[r])

    return result


@bp.route('/')
def index_view():
    session = Session()
    tournaments = session.query(Tournament).all()

    admin = request.args.get('admin', '') == 'True'

    return render_template('tournaments/index.html', admin=admin, tournaments=tournaments)


@bp.route('/<int:tid>')
def view_tournament(tid):
    session = Session()
    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()

    tournament = session.query(Tournament).filter(Tournament.id == tid).one()
    games = session.query(Game).filter(Game.tournament_id == tid).all()
    players = session.query(Player).all()

    players_map = {}
    pmap = {}

    for player in players:
        players_map[player.id] = player

    for p in participants:
        pmap[p.id] = players_map[p.player_id]

    admin = request.args.get('admin', '') == 'True'

    data = Ranking().getTournamentRanking(tid)

    rounds = groupByRound(games)

    return render_template('tournaments/view_tournament.html', admin=admin, participants=pmap, players=players_map,
                           tournament=tournament,
                           rounds=rounds, data=data)
