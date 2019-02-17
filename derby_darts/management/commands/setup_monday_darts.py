import os
from django.core.management import BaseCommand
from derby_darts.models import League, Season, Team, SeasonStanding
from Darts.settings import BASE_DIR
from Fixtures.csv_importer import CSVImporter

__author__ = 'Michael'


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.__init_league_for_summer__()

    def __init_league_for_summer__(self):
        league, created = League.objects.get_or_create(short_url='dda')

        season, created = Season.objects.get_or_create(league=league, season='Summer', year=2015)

        print('Season created')

        teams = self.__add_teams_to_league__(season)
        self.__add_fixtures__(teams, season)

    @staticmethod
    def __add_teams_to_league__(season):
        section_one = ['Chellaston Club A',
                       'New Bridge Inn',
                       'Lamb (Melbourne)',
                       'Malt Shovel (Spondon)',
                       'Smithfield',
                       'Bye',
                       'Prince of Wales (Spondon)',
                       'Chellaston Club B']

        sections = [section_one]

        team_section = []
        for idx, section in enumerate(sections):
            teams = []
            for team in section:
                team_obj, created = Team.objects.get_or_create(name=team, league=season.league)

                print(team, ' added')

                teams.append(team_obj)

                standing = SeasonStanding.objects.get_or_create(season=season, team=team_obj, section=idx+1)
            team_section.append(teams)

        return team_section

    @staticmethod
    def __add_fixtures__(team_sections, season):
        importer = CSVImporter(os.path.join(BASE_DIR, 'Fixtures', 'Excel', 'MondayFixtures.csv'))

        for section in team_sections:
            importer.load_file_for_season(section, season)
