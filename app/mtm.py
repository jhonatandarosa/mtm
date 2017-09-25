import codecs
import functools
import json
import random
import os
import signal
import sys

decks = []
players = []
tournaments = []
stats = {
    'players': {},
    'decks': {}
}
sts = ['mw', 'ml', 'w', 'l', 'pts']


def get_winner(t):
    rounds = t['rounds']
    pts = {}

    for p in players:
        pts[p] = 0

    for r in rounds:
        games = r['games']

        for game in games:
            p1 = game['p1']
            p2 = game['p2']

            pts[p1['name']] += p1['wins']
            pts[p2['name']] += p2['wins']

    winner_pts = 0
    winner = None

    for player in pts:
        if pts[player] > winner_pts:
            winner_pts = pts[player]
            winner = player

    return winner


def get_participant_deck(t, player):
    parts = t['players']

    for p in parts:
        if p['name'] == player:
            return p['deck']


def get_available_decks_for_next_tournament():
    d = []
    d.extend(decks)

    for t in tournaments:
        winner = get_winner(t)

        deck = get_participant_deck(t, winner)
        d.remove(deck)

    return d


def get_last_decks_from_player(player):
    d = []

    count = 0
    for t in reversed(tournaments):
        if count == 2:
            break
        count += 1
        d.append(get_participant_deck(t, player))

    return d


def match_decks_and_players(dks, plrs):
    random.shuffle(dks)

    matches = []

    for player in plrs:
        last_decks = get_last_decks_from_player(player)

        possible_decks = [d for d in dks if d not in last_decks]

        random.shuffle(possible_decks)
        deck = possible_decks[0]
        dks.remove(deck)

        matches.append({"name": player, "deck": deck})

    return matches


def save_tournament(name, t):
    with codecs.open('data/tournaments/%s' % name, mode='w', encoding='utf8') as file:
        file.write(json.dumps(t))


def new_tournament():
    print('creating tournament...')

    player_names = select_players()

    name = 'dgtmtg%s.json' % (len(tournaments) + 1)

    dks = get_available_decks_for_next_tournament()

    results = match_decks_and_players(dks, player_names)

    t = {
        'players': results
    }
    save_tournament(name, t)

    for r in results:
        print('%s: %s' % (r['player'], r['deck']))


def general_or_by_tournament():
    print('0 - General')
    for i, t in enumerate(tournaments):
        i += 1
        print('%s - %s° DGT Magic Tournament' % (i, i))

    return int(input('> '))


def decks_stats():
    opt = general_or_by_tournament()

    if opt == 0:  # general
        print_ranking('Decks', stats['decks'])
    else:
        print_ranking('Decks', get_tournament_stats(tournaments[opt-1])['decks'])


def players_stats():
    opt = general_or_by_tournament()

    if opt == 0:  # general
        print_ranking('Players', stats['players'])
    else:
        print_ranking('Players', get_tournament_stats(tournaments[opt-1])['players'])


options = [
    {
        "name": "New Tournament",
        "handler": new_tournament
    },
    {
        "name": "Decks Ranking",
        "handler": decks_stats
    },
    {
        "name": "Players Ranking",
        "handler": players_stats
    },

]


def load_players():
    print("Loading players...")
    with codecs.open("data/players.json", encoding="utf8") as file:
        data = file.readlines()

    global players
    players = json.loads(''.join(data))


def load_decks():
    print("Loading decks...")
    with codecs.open("data/decks.json", encoding="utf8") as file:
        data = file.readlines()

    global decks
    decks = json.loads(''.join(data))


def load_tournaments():
    print('Loading tournaments...')

    global tournaments
    files = os.listdir('data/tournaments')

    for tournament in files:
        path = os.path.join('data/tournaments', tournament)

        with codecs.open(path, encoding="utf8") as file:
            data = file.readlines()
            tour = json.loads(''.join(data))
            tournaments.append(tour)


def get_round_stats(hound):
    rstats = {}
    games = hound['games']

    for game in games:
        p1 = game['p1']
        p2 = game['p2']

        for p in [(p1, p2), (p2, p1)]:
            pts = p[0]['wins'] - p[1]['wins']
            rstats[p[0]['name']] = {
                'w': p[0]['wins'],
                'l': p[1]['wins'],
                'pts': pts,
                'mw': 1 if pts > 0 else 0,
                'ml': 1 if pts < 0 else 0
            }

    return rstats


def create_item_stats():
    return dict(zip(sts, [0] * len(sts)))


def get_tournament_stats(t):
    tstats = {
        'players': {},
        'decks': {}
    }

    for player in t['players']:
        tstats['players'][player['name']] = create_item_stats()
        tstats['decks'][player['deck']] = create_item_stats()

    rounds = t['rounds']

    for r in rounds:
        rstats = get_round_stats(r)

        for player in t['players']:
            pname = player['name']

            if pname not in rstats:
                continue

            dname = player['deck']
            pstats = tstats['players'][pname]
            dstats = tstats['decks'][dname]
            for s in sts:
                pstats[s] += rstats[pname][s]
                dstats[s] += rstats[pname][s]

    return tstats


def ranking_sort(a, b):
    # match wins
    if a['mw'] != b['mw']:
        return -1 if a['mw'] > b['mw'] else 1
    else:
        # games points diff
        if a['pts'] != b['pts']:
            return -1 if a['pts'] > b['pts'] else 1

    return 0


def ranking(data):
    rank = []

    for k in data.keys():
        d = dict(data[k])
        d['name'] = k
        rank.append(d)

    rank.sort(key=functools.cmp_to_key(ranking_sort))

    return rank


def print_ranking(name, data):
    # rows = data.keys()
    rank = ranking(data)
    headers = {
        'mw': 'Match Wins',
        'ml': 'Match Lost',
        'w': 'Set Wins',
        'l': 'Set Lost',
        'pts': 'Points'
    }

    headers = [headers[k] for k in sts]

    row_format = "{:>20}" + ("{:>15}" * (len(headers)))

    print('\n\n')
    print('General Ranking of %s' % name)
    print('-' * 20 + '-' * (15 * (len(headers))))
    print(row_format.format("", *headers))

    for item in rank:
        data = [item[k] for k in sts]
        print(row_format.format(item['name'], *data))


def calculate_stats():
    print('Calculating statistics...')

    global stats

    for t in tournaments:
        tstats = get_tournament_stats(t)

        pstats = tstats['players']
        dstats = tstats['decks']

        for player in pstats:
            if player not in stats['players']:
                stats['players'][player] = create_item_stats()

            for s in sts:
                stats['players'][player][s] += pstats[player][s]

        for deck in dstats:
            if deck not in stats['decks']:
                stats['decks'][deck] = create_item_stats()

            for s in sts:
                stats['decks'][deck][s] += dstats[deck][s]


def get_option():
    print("\n\nMenu:")
    for idx, opt in enumerate(options):
        print("\t%s - %s" % (idx + 1, opt['name']))

    try:
        idx = int(input(">"))
    except Exception:
        return None

    if 0 < idx <= len(options):
        return options[idx - 1]

    return None


def select_players():
    print("Select players to create the tournament")
    print("\tAvailable players: %s" % players)
    print("Type the name of the player, 'all' to add all available Players, or 'done' to finish.")

    names = []
    name = None
    while name != 'all' and name != 'done':
        name = input()
        if name == 'all':
            names = []
            names.extend(players)
        elif name != 'done':
            if name in players:
                names.append(name)
            else:
                print('%s not available' % name)

    return names


def main_loop():
    print("-------------------------------------------")
    print("|                                         |")
    print("|   DGT Magic Tournament Manager v1.0.0   |")
    print("|                                         |")
    print("-------------------------------------------")
    print("\n")

    while True:
        opt = get_option()
        if opt is not None:
            opt['handler']()
        else:
            break


def load_data():
    load_decks()
    load_players()
    load_tournaments()
    calculate_stats()


def main():
    def signal_handler(signal, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    load_data()

    main_loop()


if __name__ == '__main__':
    main()
