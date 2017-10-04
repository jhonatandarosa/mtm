from flask import Blueprint
from flask import render_template
from flask import request

from app import Session
from app.model import Player
from app.model import Participant
from app.model import Tournament
from app.model import Game
from app.model import Deck
from app.model import helper

from app.core import Ranking

main = Blueprint('blueprint_%s' % __name__, __name__, template_folder='templates')


@main.route('/')
def index_view():
    session = Session()
    tournament = session.query(Tournament).filter(Tournament.status == 'active').first()
    if tournament is None:
        return render_template('main.html')

    tid = tournament.id

    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()

    games = session.query(Game).filter(Game.tournament_id == tid).order_by(Game.id.asc()).all()
    players = session.query(Player).all()
    decks = session.query(Deck).all()

    players_map = {}
    decks_map = {}
    pmap = {}

    for player in players:
        players_map[player.id] = player

    for deck in decks:
        decks_map[deck.id] = deck

    for p in participants:
        pmap[p.id] = {
            'player': players_map[p.player_id],
            'deck': decks_map[p.deck_id]
        }

        if p.player2_id is not None:
            pmap[p.id]['player2'] = players_map[p.player2_id]
            pmap[p.id]['deck2'] = decks_map[p.deck2_id]

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
