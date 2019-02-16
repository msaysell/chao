from derby_darts.models import Fixture

__author__ = 'Michael.Saysell'
import csv
from datetime import datetime


class CSVImporter(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        return csv.reader(self.file_name, 'r')

    def load_file(self):
        with open(self.file_name, 'rb') as csv_file:
            contents = csv.reader(csv_file)

            if not contents:
                return False

            date_strings = contents.next()
            dates = map(lambda date_string: datetime.strptime(date_string, '%d/%m/%Y'), date_strings)

            section_one = ['Alv/Crewton', 'OMS A', 'Sinfin Moor', 'Coach and Horses', 'Brunswick',
                           'Duke of Clarence B', 'Courtyard B', 'Chad Lace', 'Station Inn', 'York Tavern']

            section_two = ['Woodlark', 'Courtyard A', 'Navigation', 'Spa Inn', '102 Club',
                           'Littleover Social', 'OMS B', 'Furnace', 'Norman Arms']

            section_three = ['Duke of Clarence A', 'Dunkirk', 'Junction Tav', 'Golden Eagle', '105 Club',
                             'Alexandra', 'Seven Stars', 'Clarion Club', 'The Mile', 'BYE']

            for row_idx, row in enumerate([x for x in contents]):
                for idx, fixture in enumerate(row):
                    if 'H' in fixture:
                        print('{}: {} v {}'.format(dates[idx],
                                                   section_three[row_idx],
                                                   section_three[int(fixture[:-1]) - 1]))

    def load_file_for_season(self, teams, season):

        with open(self.file_name, 'rb') as csv_file:
            contents = csv.reader(csv_file)

            if not contents:
                return False

            date_strings = contents.next()
            dates = map(lambda date_string: datetime.strptime(date_string, '%d/%m/%Y'), date_strings)

            fixture_rows = [x for x in contents]

            for row_idx, row in enumerate(fixture_rows):
                for idx, fixture in enumerate(row):
                    if 'H' in fixture:
                        fixture, created = Fixture.objects.get_or_create(season=season,
                                                                         date=dates[idx],
                                                                         home_team=teams[row_idx],
                                                                         away_team=teams[int(fixture[:-1]) - 1])
                        fixture.save()
