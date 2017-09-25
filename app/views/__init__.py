

def init(app):
    from .main import main
    from .players import bp as players

    app.register_blueprint(main)
    app.register_blueprint(players)