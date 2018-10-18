from rest_framework import routers

from Darts.api.view_sets import WallPostViewSet, TeamLeagueStandingViewSet, SeasonViewSet, TeamsViewSet

router = routers.SimpleRouter()
router.register('wallposts', WallPostViewSet)
router.register('team_standings', TeamLeagueStandingViewSet, base_name='team_standings')
router.register('seasons', SeasonViewSet, base_name='seasons')
router.register('teams', TeamsViewSet, base_name='teams')
