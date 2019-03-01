from django.db.models import Case
from django.db.models import Count, IntegerField, Sum
from django.db.models import F
from django.db.models import Q
from django.db.models import When
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from derby_darts.models import WallPost, Team, Season
from derby_darts.serializers import WallPostSerializer, TeamLeagueSerializer, LeagueSeasonSerializer, TeamSerializer


class TeamsViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        current_season = Season.objects.filter(league=self.request.league).order_by('-start_date').first()
        return Team.objects.filter(league=self.request.league, seasonstanding__season=current_season).order_by('name')


class WallPostViewSet(ModelViewSet):
    queryset = WallPost.objects.order_by('-date_created')
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = WallPostSerializer


class TeamLeagueStandingViewSet(ModelViewSet):
    serializer_class = TeamLeagueSerializer

    def get_season(self, pk=None):
        if pk:
            season = Season.objects.get(pk=pk)
        else:
            season = Season.objects.filter(league=self.request.league).order_by('-start_date').first()
        return season

    def get_queryset(self):
        season = self.get_season(self.request.GET.get('pk'))
        teams = Team.objects.filter(league=self.request.league, seasonstanding__season=season)

        home_games_played = Sum(Case(When(Q(home_team__season=season, home_team__result__isnull=False), then=1),
                                     default=0, output_field=IntegerField()))
        away_games_played = Sum(Case(When(Q(away_team__season=season, away_team__result__isnull=False), then=1),
                                     default=0, output_field=IntegerField()))

        return teams.annotate(hgp=home_games_played,
                              agp=away_games_played).annotate(games_played=F('hgp'))

    def get_serializer_context(self):
        context = super(TeamLeagueStandingViewSet, self).get_serializer_context()
        context['season_standing'] = self.get_season(self.request.GET.get('pk'))
        return context


class SeasonViewSet(ModelViewSet):
    serializer_class = LeagueSeasonSerializer

    def get_queryset(self):
        return Season.objects.filter(league=self.request.league)
