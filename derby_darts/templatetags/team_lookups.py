from django.db.models import Q, Sum
from derby_darts.models import Fixture, SeasonPointDeduction

__author__ = 'Michael.Saysell'
from django import template

register = template.Library()


@register.simple_tag(name='get_total_points')
def get_total_points(team):

    team_fixtures = Fixture.objects.filter(home_team=team, result__isnull=False)

    if not team_fixtures:
        return 0.0

    points = 0.0

    for fixture in team_fixtures:
        if fixture.result.home_team_score > fixture.result.away_team_score:
            points += 2.0

    return points


@register.simple_tag(name='get_season_section')
def get_season_section(team):
    return team.seasonstanding_set.all()[0].section


@register.filter(name='get_league_data_for_team')
def get_league_data_for_team(standing, season):
    team = standing.team
    points_lost = SeasonPointDeduction.objects.filter(standing=standing).aggregate(lost_points=Sum('num_of_points'))
    points_lost = points_lost.get('lost_points') or 0

    class TeamData(object):
        def __init__(self, name):
            self.team_name = name
            self.games_played = 0
            self.games_won = 0
            self.games_lost = 0
            self.points_for = 0
            self.points_against = 0
            self.points = 0
            self.points_deducted = 0

    team_fixtures = Fixture.objects.filter(Q(home_team=team) | Q(away_team=team),
                                           season=season,
                                           result__isnull=False, result__void_result=False)

    data = TeamData(team)
    data.points -= points_lost
    data.points_deducted = points_lost
    if not team_fixtures:
        return data

    for fixture in team_fixtures:
        data.games_played += 1
        if fixture.home_team == team:
            if fixture.result.home_team_score > fixture.result.away_team_score:
                data.games_won += 1
                data.points += 2
            else:
                data.games_lost += 1
            data.points += fixture.result.home_team_score
            data.points_for += fixture.result.home_team_score
            data.points_against += fixture.result.away_team_score
        else:
            if fixture.result.home_team_score > fixture.result.away_team_score:
                data.games_lost += 1
            else:
                data.games_won += 1
                data.points += 2
            data.points += fixture.result.away_team_score
            data.points_for += fixture.result.away_team_score
            data.points_against += fixture.result.home_team_score

    return data


@register.simple_tag(name='get_league_data')
def get_league_data(team_standings, season):

    data = [get_league_data_for_team(standing, season) for standing in team_standings]

    return sorted(data, key=lambda team_data: -team_data.points)
