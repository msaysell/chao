from django.db.models import F, Sum
from django.db.models import Q
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import fields

from derby_darts.models import WallPost, Fixture, Team, SeasonStanding, Season, Section, Player


class WallPostSerializer(ModelSerializer):
    class Meta:
        model = WallPost


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ['name']


class TeamSerializer(ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'players']


class TeamLeagueSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'season_section', 'games_played', 'games_won', 'games_lost',
                  'points_for', 'points_against', 'points']
    games_played = fields.SerializerMethodField()
    games_won = fields.SerializerMethodField()
    games_lost = fields.SerializerMethodField()
    points_for = fields.SerializerMethodField()
    points_against = fields.SerializerMethodField()
    points = fields.SerializerMethodField('get_total_points')
    season_section = fields.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(TeamLeagueSerializer, self).__init__(*args, **kwargs)
        self.season = self.context['season_standing']
        self.team_fixtures = self.fixtures(self.instance)

    def fixtures(self, team):
        return Fixture.objects.filter(Q(home_team=team) | Q(away_team=team),  season=self.season,
                                      result__isnull=False, result__void_result=False)

    def get_season_section(self, obj):
        return SeasonStanding.objects.only('section').get(team=obj, season=self.season).section

    def get_games_played(self, obj):
        return obj.hgp + obj.agp

    def get_games_won(self, obj):
        home_results = Q(home_team=obj, result__home_team_score__gt=F('result__away_team_score'))
        away_results = Q(away_team=obj, result__away_team_score__gt=F('result__home_team_score'))
        results = self.fixtures(obj).filter(home_results | away_results)
        return results.count()

    def get_games_lost(self, obj):
        home_results = Q(home_team=obj, result__home_team_score__lt=F('result__away_team_score'))
        away_results = Q(away_team=obj, result__away_team_score__lt=F('result__home_team_score'))
        results = self.fixtures(obj).filter(home_results | away_results)
        return results.count()

    def get_points_for(self, obj):
        # home_results = Q(home_team=obj, result__isnull=False)
        # away_results = Q(away_team=obj, result__away_team_score__gt=F('result__home_team_score'))
        home_score = self.fixtures(obj).filter(home_team=obj).aggregate(home=Sum('result__home_team_score'))['home'] or 0
        away_score = self.fixtures(obj).filter(away_team=obj).aggregate(away=Sum('result__away_team_score'))['away'] or 0
        return home_score + away_score

    def get_points_against(self, obj):
        # home_results = Q(home_team=obj, result__home_team_score__lt=F('result__away_team_score'))
        # away_results = Q(away_team=obj, result__away_team_score__lt=F('result__home_team_score'))
        home_score = self.fixtures(obj).filter(home_team=obj).aggregate(home=Sum('result__away_team_score'))['home'] or 0
        away_score = self.fixtures(obj).filter(away_team=obj).aggregate(away=Sum('result__home_team_score'))['away'] or 0
        return home_score + away_score

    def get_total_points(self, obj):
        return self.get_points_for(obj) + (self.get_games_won(obj) * 2)


class LeagueSeasonSerializer(Serializer):
    id = fields.SerializerMethodField()
    name = fields.SerializerMethodField()
    leagues = fields.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_leagues(self, obj):
        leagues = {}

        for standing in obj.seasonstanding_set.order_by('season_section_id').prefetch_related('season_section'):
            season_name = standing.season_section.name
            if season_name not in leagues:
                leagues[season_name] = []
            leagues[season_name].append(TeamLeagueSerializer(instance=standing.team,
                                                             context={'season_standing': obj}).data)

        for key, league in leagues.items():
            league.sort(key=lambda n: -n['points'])
        return leagues
