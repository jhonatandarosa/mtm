from flask import Flask
from flask import render_template

# Import MongoKit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
app.config.from_object('config.DevelopmentConfig')

# Define the database object which is imported
# by modules and controllers
# connect to the database
db = SQLAlchemy(app)
Session = db.sessionmaker(bind=db.engine)

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

# from app.core import TournamentManager

# TournamentManager().test()
