
def init(app):
    from .players import bp as players
    from .games import bp as games

    app.register_blueprint(players)
    app.register_blueprint(games)