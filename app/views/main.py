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


@main.route('/query/dropall')
def dropall():
    session = Session()
    print(session.execute('DROP TABLE game;'))
    print(session.execute('DROP TABLE participant;'))
    print(session.execute('DROP TABLE tournament;'))
    print(session.execute('DROP TABLE deck;'))
    print(session.execute('DROP TABLE player;'))

@main.route('/query/dump')
def dump():
    session = Session()
    sql_file = open('data/dump.sql', 'r')

    # Create an empty command string
    sql_command = ''

    # Iterate over all lines in the sql file
    for line in sql_file:
        # Ignore comented lines
        if not line.startswith('--') and line.strip('\n'):
            # Append line to the command string
            line = line.strip('\n')
            if '--' in line:
                line = line[0: line.rindex('--')]
            sql_command += line

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statemente and commit it
                try:
                    session.execute(sql_command)
                    session.commit()

                # Assert in case of error
                except Exception as e:
                    print(sql_command)
                    print('Ops')

                # Finally, clear command string
                finally:
                    sql_command = ''

@main.route('/query/fix')
def fix():
    session = Session()
    sql_file = open('data/pgsql_fix_serials.sql', 'r')

    # Create an empty command string
    sql_command = ''

    # Iterate over all lines in the sql file
    for line in sql_file:
        sql_command += line

    try:
        session.execute(sql_command)
        session.commit()
    except Exception as e:
        print(sql_command)
        print('Ops')
    try:
        session.execute('SELECT fix_serials();')
        session.commit()
    except Exception as e:
        print('Fix serials')


@main.after_request
def remove_session(response):
    Session.remove()
    return response
