import functools

from app import Session
from app.model import Tournament
from .Ranking import Ranking
from .SingletonDecorator import SingletonDecorator


class RankingManager:
    rankings = {}

    def __init__(self) -> None:
        super().__init__()

        session = Session()
        session.flush()

        years = session.query(Tournament.year).distinct().all()

        years = [x[0] for x in years]
        years.append(None)

        for year in years:
            self.rankings[year] = Ranking(year)

    def refresh(self):
        print('refresh rankings...')
        for key in self.rankings:
            print('refresh %s ranking...' % key)
            ranking = self.rankings[key]
            ranking.refresh()

    def get_tournament_ranking(self, id):
        for key in self.rankings:
            ranking = self.rankings[key]
            if ranking.contains_tournament(id):
                return ranking.get_tournament_ranking(id)

    def ranking_table(self, data, show_tournaments=False):
        table = {
            'headers': ['Name', 'M. Played', 'M. Won', 'M. Lost', 'G. Played', 'G. Won', 'G. Lost', 'Pts', '% Pts'],
            'cols': ['mp', 'mw', 'ml', 'p', 'w', 'l', 'pts', 'ppts']
        }

        if show_tournaments:
            table['headers'].insert(1, 'T. Won')
            table['headers'].insert(1, 'T. Played')
            table['cols'].insert(0, 't')
            table['cols'].insert(0, 'tp')

        rows = []

        for rank in data:
            row = dict(rank)

            if row['mp'] > 0:
                ppts = row['pts'] / (row['mp'] * 9) * 100
            else:
                ppts = 0
            row['ppts'] = "{0:.2f}".format(round(ppts, 2))
            rows.append(row)

        table['rows'] = rows
        return table

    def get_ranking(self, year=None) -> Ranking:
        return self.rankings[year]

    def get_titles(self, id) -> []:
        titles = []
        for key in self.rankings:
            ranking = self.rankings[key]
            if ranking.year is None:
                continue
            if id not in ranking.titles:
                continue
            r_titles = ranking.titles[id]
            for title in r_titles:
                titles.append('%s (%s)' % (title, ranking.year))
        return titles



RankingManager = SingletonDecorator(RankingManager)
