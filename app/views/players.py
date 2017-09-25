from flask import Blueprint
from flask import render_template

from app import Session
from app.model import Player

bp = Blueprint('blueprint_%s' % __name__, __name__, url_prefix='/players', template_folder='templates/',
               static_folder='/static')


@bp.route('/')
def index_view():
    session = Session()
    result = session.query(Player).all()
    return render_template('players/index.html', players=result)
