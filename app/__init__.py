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
Ranking().refresh()
Session.remove()


# from app.core import TournamentManager
# from app.model import TournamentType

# TournamentManager().new_tournament(TournamentType.TWO_HEADED_GIANT, '1° Two Headed Giants', [1, 2, 3, 4, 5, 6], 'T3')
