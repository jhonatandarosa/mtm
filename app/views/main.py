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

main = Blueprint('blueprint_%s' % __name__, __name__, template_folder='templates')


@main.route('/')
def index_view():
    session = Session()
    tournament = session.query(Tournament).filter(Tournament.status == 'active').one()
    tid = tournament.id

    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()

    games = session.query(Game).filter(Game.tournament_id == tid).all()
    players = session.query(Player).all()

    players_map = {}
    pmap = {}

    for player in players:
        players_map[player.id] = player

    for p in participants:
        pmap[p.id] = players_map[p.player_id]

    admin = request.args.get('admin', '') == 'True'

    data = Ranking().get_tournament_ranking(tid)

    rounds = helper.group_by_round(games)

    return render_template(
        'tournaments/view_tournament.html',
        admin=admin,
        participants=pmap,
        players=players_map,
        tournament=tournament,
        rounds=rounds, data=data
    )
