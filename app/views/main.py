from flask import Blueprint
from flask import render_template

main = Blueprint('blueprint_%s' % __name__, __name__, template_folder='templates')


@main.route('/')
def index_view():

    return render_template('main.html', releases=[])
