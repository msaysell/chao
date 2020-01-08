from rest_framework import routers

from Darts.api.view_sets import WallPostViewSet, TeamLeagueStandingViewSet, SeasonViewSet, TeamsViewSet, EventsViewSet

router = routers.SimpleRouter()
router.register('wallposts', WallPostViewSet)
router.register('team_standings',
                TeamLeagueStandingViewSet,
                basename='team_standings')
router.register('seasons', SeasonViewSet, basename='seasons')
router.register('teams', TeamsViewSet, basename='teams')
router.register('events', EventsViewSet, basename='events')
