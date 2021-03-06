__author__ = 'Saysell'

from django.urls import path as url, re_path
from Fixtures import views

urlpatterns = [url(r"fixtures_by_team", views.fixtures_by_team, name='fixtures_by_team'),
               url(r"fixtures_by_team/<int:season_id>", views.season_fixtures_by_team, name='season_fixtures_by_team'),
               url(r"latest_sections", views.latest_sections, name='latest_sections'),
               url(r"sections_and_teams/<int:season_id>", views.latest_sections, name='sections_and_teams'),
               url(r"teams_for_section/<int:section>", views.teams_for_section, name='teams_for_section'),
               url(r"teams_for_section/<int:season_id>/<int:section>", views.seasonal_teams_for_section, name='seasonal_teams_for_section'),
               url(r"fixtures_for_team/<str:team_name>", views.fixtures_for_team, name='fixtures_for_team'),
               url(r"fixtures_for_team/<int:season_id>/<str:team_name>", views.seasonal_fixtures_for_team, name='seasonal_fixtures_for_team'),
               url(r"fixtures_by_date", views.fixtures_by_date, name='fixtures_by_date'),
               url(r'missing', views.missing_results, name="missing_results"),
               url(r"existing_fixtures", views.existing_fixtures, name='existing_fixtures'),
               url(r'set_results', views.set_results, name='set_results'),
               url(r'update_results', views.UpdateResultsView.as_view(paginate_by='10'), name='update_results'),

               url(r'get_update_results_form/<int:post_d>', views.get_update_results_form, name='get_update_results_form'),
               url(r'set_score', views.set_score, name='set_score'),
               url(r'set_common_fixture', views.set_common_fixture, name='set_common_fixture'),
               url(r'import/<int:season_id>', views.import_season, name='import_season'),
               url(r'import', views.import_fixtures, name='import_fixtures'),
               url(r'swap_teams', views.SwapTeamView.as_view(), name='swap_teams'),
               url(r'creator', views.FixtureMakerView.as_view(), name='creator')
               ]

