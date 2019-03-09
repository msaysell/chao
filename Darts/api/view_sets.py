from django.db.models import Case, Count, IntegerField, Sum, OuterRef, Subquery, F, Q, When
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from derby_darts.models import WallPost, Team, Season, Fixture
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
        played = Fixture.objects.filter(season=season, result__isnull=False).exclude(
            Q(away_team__name__icontains="bye") | Q(home_team__name__icontains="bye"))
        home_played = played.filter(home_team=OuterRef('pk')).values('pk')
        away_played = played.filter(away_team=OuterRef('pk')).values('pk')
        
        return teams.annotate(hgp=Count(Subquery(home_played)),
                              agp=Count(Subquery(away_played)))

    def get_serializer_context(self):
        context = super(TeamLeagueStandingViewSet, self).get_serializer_context()
        context['season_standing'] = self.get_season(self.request.GET.get('pk'))
        return context


class SeasonViewSet(ModelViewSet):
    serializer_class = LeagueSeasonSerializer

    def get_queryset(self):
        return Season.objects.filter(league=self.request.league)
