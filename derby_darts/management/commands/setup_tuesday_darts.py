import os
from django.core.management import BaseCommand
from Darts.settings import BASE_DIR
from Fixtures.csv_importer import CSVImporter
from derby_darts.models import League, Season, Team, SeasonStanding

__author__ = 'Saysell'


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.__init_league_for_summer__()

    def __init_league_for_summer__(self):
        league, created = League.objects.get_or_create(name='Derby Tuesday Pub and Club League')

        print('League created')

        season, created = Season.objects.get_or_create(league=league, season='Summer', year=2015)

        print('Season created')

        teams = self.__add_teams_to_league__(season)
        self.__add_fixtures__(teams, season)

    @staticmethod
    def __add_teams_to_league__(season):
        section_one = ['Alvaston Crewton', 'OMS A', 'Sinfin Moor', 'Coach and Horses', 'Brunswick',
                       'Duke of Clarence B', 'Courtyard B', 'Chad Lace', 'Station Inn', 'York Tavern']
        section_two = ['Woodlark', 'Courtyard A', 'BYE 2', 'Spa Inn', '102 Club',
                       'Littleover Social', 'OMS B', 'Furnace', 'Norman Arms', 'Chestnut']
        section_three = ['Duke of Clarence A', 'Dunkirk', 'Junction Tav', 'Golden Eagle', '105 Club',
                         'Alexandra', 'Seven Stars', 'Clarion Club', 'The Mile', 'BYE']

        sections = [section_one, section_two, section_three]

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
        importer = CSVImporter(os.path.join(BASE_DIR, 'Fixtures', 'Excel', 'Fixtures.csv'))

        for section in team_sections:
            importer.load_file_for_season(section, season)
