def group_by_round(games):
    rounds = {}

    for game in games:
        if game.round not in rounds:
            rounds[game.round] = []

        rounds[game.round].append(game)

    result = []
    for r in rounds:
        result.append(rounds[r])

    return result
