

def init(app):
    from .main import main
    from .players import bp as players
    from .decks import bp as decks
    from .tournaments import bp as tournaments

    app.register_blueprint(main)
    app.register_blueprint(players)
    app.register_blueprint(decks)
    app.register_blueprint(tournaments)