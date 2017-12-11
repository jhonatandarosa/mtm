from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

app = Flask(__name__)

# Configurations
app.config.from_object('config.DevelopmentConfig')

# Define the database object which is imported
# by modules and controllers
# connect to the database
db = SQLAlchemy(app)
Session = scoped_session(db.sessionmaker(bind=db.engine))

# Import a module / component using its blueprint handler variable (mod_auth)
from app.views import init as init_views
from app.api import init as init_api

# Register blueprint(s)

init_views(app)
init_api(app)

# create database
db.create_all()

from app.core import Ranking

# init ranking
# Ranking().refresh()
# Session.remove()
session = Session()
#
# print('loading dump')
# sql_file = open('data/dump.sql', 'r')
#
# # Create an empty command string
# sql_command = ''
#
# # Iterate over all lines in the sql file
# for line in sql_file:
#     # Ignore comented lines
#     if not line.startswith('--') and line.strip('\n'):
#         # Append line to the command string
#         line = line.strip('\n')
#         if '--' in line:
#             line = line[0: line.rindex('--')]
#         sql_command += line
#
#         # If the command string ends with ';', it is a full statement
#         if sql_command.endswith(';'):
#             # Try to execute statemente and commit it
#             try:
#                 session.execute(sql_command)
#                 session.commit()
#
#             # Assert in case of error
#             except Exception as e:
#                 print(sql_command)
#                 print('Ops')
#
#             # Finally, clear command string
#             finally:
#                 sql_command = ''
#
# print('fixing serials')
# sql_file = open('data/pgsql_fix_serials.sql', 'r')
#
# # Create an empty command string
# sql_command = ''
#
# # Iterate over all lines in the sql file
# for line in sql_file:
#     sql_command += line
#
# try:
#     session.execute(sql_command)
#     session.commit()
# except Exception as e:
#     print(sql_command)
#     print('Ops')
# try:
#     session.execute('SELECT fix_serials();')
#     session.commit()
# except Exception as e:
#     print('Fix serials')

# from app.core import TournamentManager
# from app.model import TournamentType

# TournamentManager().new_tournament(TournamentType.TWO_HEADED_GIANT, '1° Two Headed Giants', [1, 2, 3, 4, 5, 6], 'T3')
