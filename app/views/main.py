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
from app.core import match_score

main = Blueprint('blueprint_%s' % __name__, __name__, template_folder='templates')


@main.route('/')
def index_view():
    session = Session()

    tournament = session.query(Tournament).filter(Tournament.status == 'active').first()
    if tournament is None:
        return render_template('main.html')

    from .tournaments import render_tournament

    return render_tournament(tournament=tournament)


@main.route('/about')
def about_view():
    return render_template(
        'about.html',
        match_score=match_score
    )


@main.after_request
def remove_session(response):
    Session.remove()
    return response
