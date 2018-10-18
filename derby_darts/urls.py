from django.conf.urls import url
from derby_darts import views
from derby_darts.views import PostFormView, PostListView, TeamDetailView, TeamListView, AddPlayerView

urlpatterns = [url(r'^$',  PostListView.as_view(), name='home'),
               url(r'^teams/$', TeamListView.as_view(), name='team_list'),
               url(r'^team/(?P<pk>\d+)$', TeamDetailView.as_view(), name='team_details'),
               url(r'^team/(?P<pk>\d+)/add_players$', AddPlayerView.as_view(), name='add_players'),
               url(r'^modify_wall_post$', PostFormView.as_view(), name='modify_wall_post'),
               url(r'^get_edit_post_form/(\d+)$', views.get_edit_post_form, name='get_edit_post_form'),
               url(r'^delete_post/(\d+)$', views.delete_post, name='delete_post'),
               url(r'^leagues/(\d+)$', views.selected_league, name='select_league'),
               url(r'^leagues$', views.league, name='league'),
               url(r'^validate/$', views.validate_number, name='validate_number'),
               url(r'^ping/$', views.ping, name='ping'),
               url(r'^new_competition$', views.new_competition, name='new_competition'),
               url(r'^new_fixture$', views.new_fixture, name='new_fixture'),
               url(r'^new_competition_fixture$', views.new_competition_fixture, name='new_competition_fixture'),
               url(r'^new_league$', views.new_league, name='new_league'),
               url(r'^new_player$', views.new_player, name='new_player'),
               url(r'^new_result$', views.ResultFormView.as_view(), name='new_result'),
               url(r'^new_season$', views.new_season, name='new_season'),
               url(r'^new_team$', views.new_team, name='new_team'),
               ]
