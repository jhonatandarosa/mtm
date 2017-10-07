
def init(app):
    from .players import bp as players
    from .games import bp as games
    from .tournaments import bp as tournaments
    from .decks import bp as decks

    app.register_blueprint(players)
    app.register_blueprint(games)
    app.register_blueprint(tournaments)
    app.register_blueprint(decks)