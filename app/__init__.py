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

session = Session()
print(session.execute('DROP TABLE game;'))
print(session.execute('DROP TABLE participant;'))
print(session.execute('DROP TABLE tournament;'))
print(session.execute('DROP TABLE deck;'))
print(session.execute('DROP TABLE player;'))
Session.remove()