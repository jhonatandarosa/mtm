from flask import Blueprint
from flask import render_template
from flask import request
from flask import abort

from app import Session
from app.model import Player
from app.model import Participant
from app.model import Tournament
from app.model import Game
from app.model import Deck
from app.model import helper
from app.core.TournamentManager import TournamentType

from app.core import Ranking

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/tournaments', template_folder='templates/',
               static_folder='/static')


def to_entity_map(entities):
    entity_map = {}
    for entity in entities:
        entity_map[entity.id] = entity
    return entity_map


def get_players_and_decks(session):
    players = session.query(Player).all()
    decks = session.query(Deck).all()

    players_map = to_entity_map(players)
    decks_map = to_entity_map(decks)

    return players_map, decks_map


def get_teams_data(participants, players, decks=None):
    teams = {}
    for p in participants:
        p1 = players[p.player_id]

        if p.player2_id is not None:
            d1 = decks[p.deck_id]
            p2 = players[p.player2_id]
            d2 = decks[p.deck2_id]
            p1name = p1.nickname if p1.nickname is not None else p1.name
            p2name = p2.nickname if p2.nickname is not None else p2.name
            teams[p.id] = {
                'name': '%s, %s' % (p1name, p2name),
                'deck': '%s, %s' % (d1.name, d2.name)
            }
        else:
            p1name = p1.nickname if p1.nickname is not None else p1.name
            teams[p.id] = {
                'name': p1name,
            }
            if decks is not None:
                d1 = decks[p.deck_id]
                teams[p.id]['deck'] = d1.name

    return teams


def process_single_tournament(session, tournament):
    tid = tournament.id

    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()
    games = session.query(Game).filter(Game.tournament_id == tid).order_by(Game.id.asc()).all()

    players, decks = get_players_and_decks(session)

    args = {}
    args['admin'] = request.args.get('admin', '') == 'True'
    args['tournament'] = tournament
    args['rounds'] = helper.group_by_round(games)
    args['teams'] = get_teams_data(participants, players, decks)

    ranking = Ranking()
    table = ranking.ranking_table(ranking.get_tournament_ranking(tid))

    args['rank_table'] = table

    return 'tournaments/single_tournament.html', args


def process_thg_tournament(session, tournament):
    tid = tournament.id

    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()
    games = session.query(Game).filter(Game.tournament_id == tid).order_by(Game.id.asc()).all()

    players, decks = get_players_and_decks(session)

    players_data = {}
    for p in participants:
        players_data[p.player_id] = {
            'name': players[p.player_id].name,
            'deck': decks[p.deck_id].name
        }
        players_data[p.player2_id] = {
            'name': players[p.player2_id].name,
            'deck': decks[p.deck2_id].name
        }

    args = {}
    args['admin'] = request.args.get('admin', '') == 'True'
    args['tournament'] = tournament
    args['rounds'] = helper.group_by_round(games)
    args['teams'] = get_teams_data(participants, players, decks)

    ranking = Ranking()
    tournament_ranking = ranking.get_tournament_ranking(tid)
    table = ranking.ranking_table(tournament_ranking['teams'])
    players_table = ranking.ranking_table(tournament_ranking['players'])

    args['rank_table'] = table
    args['players_rank_table'] = players_table
    args['players'] = players_data

    return 'tournaments/thg_tournament.html', args


def process_draft_tournament(session, tournament):
    tid = tournament.id

    participants = session.query(Participant).filter(Participant.tournament_id == tid).all()
    games = session.query(Game).filter(Game.tournament_id == tid).order_by(Game.id.asc()).all()

    players, _ = get_players_and_decks(session)
    teams = get_teams_data(participants, players)

    args = {}
    args['admin'] = request.args.get('admin', '') == 'True'
    args['tournament'] = tournament
    args['rounds'] = helper.group_by_round(games)
    args['teams'] = teams

    ranking = Ranking()
    table = ranking.ranking_table(ranking.get_tournament_ranking(tid))

    args['rank_table'] = table

    return 'tournaments/draft_tournament.html', args


def render_tournament(**kwargs):
    if 'tournament' not in kwargs and 'id' not in kwargs:
        abort(500)

    session = Session()

    if 'id' in kwargs:
        tournament = session.query(Tournament).filter(Tournament.id == kwargs['id']).one()
    else:
        tournament = kwargs['tournament']

    ttype = TournamentType(tournament.type)

    if ttype == TournamentType.SINGLE:
        template, args = process_single_tournament(session, tournament)
    elif ttype == TournamentType.TWO_HEADED_GIANT:
        template, args = process_thg_tournament(session, tournament)
    elif ttype == TournamentType.DRAFT:
        template, args = process_draft_tournament(session, tournament)

    return render_template(template, **args)


@bp.route('/')
def index_view():
    session = Session()
    tournaments = session.query(Tournament).order_by(Tournament.id.desc()).all()
    players = session.query(Player).order_by(Player.name.asc()).all()

    admin = request.args.get('admin', '') == 'True'

    return render_template(
        'tournaments/index.html',
        admin=admin,
        tournaments=tournaments,
        players=players
    )


@bp.route('/<int:tid>')
def view_tournament(tid):
    return render_tournament(id=tid)


@bp.after_request
def remove_session(response):
    Session.remove()
    return response
