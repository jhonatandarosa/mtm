
def init(app):
    from .players import bp as players

    app.register_blueprint(players)