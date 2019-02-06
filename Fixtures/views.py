from datetime import datetime
import json
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic import View, ListView
from Fixtures.csv_importer import CSVImporter
from Fixtures.fixture_maker import make_fixtures
from Fixtures.serializers import FixtureSerializer
from derby_darts.forms.forms import FixtureCreator
from derby_darts.forms.model_forms import FixtureForm, ResultForm
from derby_darts.models import Fixture, Result, Season, Team, Competition, CompetitionFixture, SeasonStanding, Section

__author__ = 'Saysell'


def fixtures_by_date(request):
    dates = Fixture.objects.values_list('date', flat=True)
    comp_dates = CompetitionFixture.objects.values_list('date', flat=True)
    all_dates = list(chain(dates, comp_dates))
    return render(request,
                  'add_date_fixtures.html',
                  {'dates': ['{dt.day}/{dt.month}/{dt.year}'.format(dt=d) for d in all_dates]})


def existing_fixtures(request):

    date = request.GET['date']
    p_date = datetime.strptime(date, "%m/%d/%Y")

    seasons = Season.objects.filter(league=request.league).values('name', 'id')
    current_season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    fixtures = Fixture.objects.filter(season=current_season,
                                      date=p_date)
    serializer = FixtureSerializer(fixtures, many=True)
    test_data = CompetitionFixture.objects.select_related('fixture').filter(season=current_season, date=p_date)
    fixture_data = [[fixture.get_home_team_name(), fixture.get_away_team_name()] for fixture in fixtures]

    return JsonResponse({"fixtures": serializer.data}, status=200)


def missing_results(request):
    fixtures = Fixture.objects.filter(season__league=request.league,
                                      result__isnull=True,
                                      date__lte=datetime.now()).order_by("-date")
    return render(request, "missing_results.html", {"fixtures": fixtures})


def set_common_fixture(request):
    if request.method == 'POST':
        date = datetime.strptime(request.POST['date'], '%d/%m/%Y')
        season_id = request.POST['season_id']
        competition_id = request.POST['competition_id']

        season = Season.objects.get(id=season_id)
        competition = Competition.objects.get(id=competition_id)

        for team in Team.objects.filter(league=request.league):
            Fixture.objects.create(competition=competition,
                                   season=season,
                                   date=date,
                                   home_team=team)

    return render(request,
                  'add_common_fixture.html',
                  {'competitions': Competition.objects.filter(season__league=request.league),
                   'seasons': Season.objects.filter(league=request.league)})


@login_required
def get_update_results_form(request, post_id):
    post = Fixture.objects.get(id=post_id)
    if request.method == 'POST':
        result, _ = Result.objects.get_or_create(fixture=post)
        form = ResultForm(request.POST, instance=result)

        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data={'id': post_id})
        return JsonResponse(status=101, data={})
    form = ResultForm(initial={'fixture': post_id})
    form.fields['fixture'].queryset = Fixture.objects.filter(id=post_id)
    return HttpResponse(str(form))


class UpdateResultsView(ListView):
    model = Fixture
    template_name = 'update_results.html'

    def get_queryset(self):
        return self.model.objects.filter(season__league=self.request.league,
                                         result__isnull=True,
                                         date__lte=datetime.now())

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateResultsView, self).dispatch(request, *args, **kwargs)


def set_results(request):
    no_results = Fixture.objects.filter(season__league=request.league,
                                        result__isnull=True,
                                        date__lte=datetime.now())

    return render(request, 'set_results.html', {'fixtures': no_results})


def set_score(request):

    if request.REQUEST:
        fixture = Fixture.objects.get(season__league=request.league, id=request.REQUEST['id'])

        home_score = request.REQUEST['home_score']
        away_score = request.REQUEST['away_score']

        result = Result(fixture=fixture,
                        home_team_score=home_score,
                        away_team_score=away_score)
        result.save()

        return JsonResponse({'data': 'Result saved'}, status=200)

    return JsonResponse(status=404, data={})


def season_fixtures_by_team(request, season_id):
    current_season = Season.objects.get(league=request.league, id=season_id)
    return __render_team_fixtures_for_season(request, current_season)


def fixtures_by_team(request):
    current_season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    return __render_team_fixtures_for_season(request, current_season)


def __render_team_fixtures_for_season(request, season):
    seasons = Season.objects.filter(league=request.league).values('name', 'id')
    sections = list(season.seasonstanding_set.values('season_section__name', 'season_section__id').distinct())

    return render(request, 'fixtures_for_team.html',
                  {
                      'sections': sections,
                      'current_season': season,
                      "all_seasons": seasons
                  })


def sections_and_teams(request):
    season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    sections = season.seasonstanding_set.distinct('season_section_id')
    serializer = SeasonStandingSerializer(sections, many=True)

    return JsonResponse({'sections': serializer.data})


def seasonal_teams_for_section(request, season_id, section):
    season = Season.objects.get(id=season_id)

    return __teams_for_section_response(season, section)


def latest_sections(request, season_id=None):
    if season_id:
        season = Season.objects.get(id=season_id)
    else:
        season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    sections = season.seasonstanding_set.distinct('section').values('season_section',
                                                                    'season_section__name',
                                                                    'season_section__order')

    return JsonResponse({'sections': list(sections)})


def teams_for_section(request, section):
    current_season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    return __teams_for_section_response(current_season, section)


def __teams_for_section_response(season, section_id):
    section_standings = season.seasonstanding_set.filter(season_section_id=section_id)
    teams = list(map(lambda standing: standing.team.name, section_standings))

    return JsonResponse({'teams': teams})


def fixtures_for_team(request, team_name):
    season = Season.objects.filter(league=request.league).order_by('-start_date').first()
    return __fixtures_for_team_response(request, season, team_name)


def seasonal_fixtures_for_team(request, season_id, team_name):
    season = Season.objects.get(id=season_id)
    return __fixtures_for_team_response(request, season, team_name)


def __fixtures_for_team_response(request, season, team_name):
    name = team_name.replace('_', ' ')
    team = Team.objects.get(league=request.league, name=name)

    fixtures = Fixture.objects.filter(Q(home_team=team) | Q(away_team=team) | Q(competitionfixture__isnull=False,
                                                                                home_team__isnull=True),
                                      season=season).order_by('date')
    fixtures = list(fixtures.values('home_team__name',
                                    'away_team__name',
                                    'competitionfixture__competition__name',
                                    'date',
                                    'result__home_team_score',
                                    'result__away_team_score'))

    return JsonResponse({'fixtures': fixtures})



@login_required
def import_fixtures(request):
    if request.method == 'POST':
        season = request.POST.get('season', None)
        if season is not None:
            season = Season.objects.get(id=int(season[0]), league=request.league)
            sections = int(request.POST.get('section_count', [0])[0])

            for team_name in request.POST.get('new_teams').split('\r\n'):
                Team.objects.get_or_create(league=request.league, name=team_name)

            teams = Team.objects.filter(league=request.league).order_by('-name')

            return render(request, 'import.html', {'teams': teams,
                                                   'season': season,
                                                   'sections': xrange(sections)})
    return render(request, 'import_select_season.html', {'seasons': Season.objects.filter(league=request.league)})


@login_required
def import_season(request, season_id):
    if request.method == 'POST':
        if not request.FILES['file_upload']:
            return JsonResponse(status=100, data={'No file received'})

        season = Season.objects.get(id=season_id, league=request.league)
        importer = CSVImporter(request.FILES['file_upload'])
        contents = importer.read_file()

        if not contents:
            return JsonResponse(status=100, data={'Unable to read the file'})

        date_strings = contents.next()
        dates = map(lambda date_string: datetime.strptime(date_string, '%d/%m/%Y') if date_string else date_string,
                    date_strings)

        sections = {k.split('_')[1]: request.POST.getlist(k) for k, v in request.POST.items() if k.startswith('sections')}

        fixtures = [x for x in contents]
        for section, team_ids in sections.items():
            section_num = int(section)
            season_section, created = Section.objects.get_or_create(league=request.league, name=section, order=section_num)
            teams = [Team.objects.get(league=request.league, id=int(team_id)) for team_id in team_ids]

            for team in teams:
                standing, created = SeasonStanding.objects.get_or_create(season=season,
                                                                         team=team,
                                                                         season_section=season_section,
                                                                         section=section_num)

            team_fixture_list = []
            for row_idx, row in enumerate(fixtures):
                team_fixtures = []
                for idx, fixture in enumerate(row):
                    if fixture.endswith('H') and len(fixture) < 4:
                        away_team_idx = int(fixture[:-1]) - 1
                        home_team = teams[row_idx]
                        away_team = teams[away_team_idx]

                        Fixture.objects.get_or_create(date=dates[idx],
                                                      season=season,
                                                      home_team=home_team,
                                                      away_team=away_team)
                        team_fixtures.append((dates[idx],
                                              home_team,
                                              away_team))
                team_fixture_list.append(team_fixtures)

        return JsonResponse(status=200, data={'fixtures': 'woo'})

    teams = Team.objects.filter(league=request.league)
    season = Season.objects.get(id=season_id, league=request.league)

    return render(request, 'import.html', {'teams': teams,
                                           'sections': 1})


class SwapTeamView(View):
    template_name = 'swap_teams.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        league = request.league
        seasons = Season.objects.filter(league=league)
        teams = Team.objects.filter(league=league)

        return render(request, self.template_name, {'seasons': seasons,
                                                    'teams': teams})

    @transaction.atomic
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        season_id = request.POST.get('season_id', None)
        team_a_id = request.POST.get('team_a_id', None)
        team_b_id = request.POST.get('team_b_id', None)

        if None in [season_id, team_a_id, team_b_id]:
            return JsonResponse(status=101, data={'value': 'Value missing'})

        season = Season.objects.get(id=int(season_id))
        team_a_standing = SeasonStanding.objects.filter(season=season, team_id=int(team_a_id))
        if not team_a_standing.exists():
            return JsonResponse(status=101, data={'value': 'Team A not in this season'})
        team_a_standing = team_a_standing[0]
        team_a = team_a_standing.team
        team_a_fixtures = Fixture.objects.filter(Q(home_team=team_a) | Q(away_team=team_a), season=season)
        
        team_b_standing = SeasonStanding.objects.filter(season=season, team_id=int(team_b_id))
        if not team_b_standing.exists():
            return JsonResponse(status=101, data={'value': 'Team A not in this season'})
        team_b_standing = team_b_standing[0]
        team_b = team_b_standing.team
        team_b_fixtures = Fixture.objects.filter(Q(home_team=team_b) | Q(away_team=team_b), season=season)

        # Swap sections
        temp_standing = team_a_standing.section
        team_a_standing.section = team_b_standing.section
        team_b_standing.section = temp_standing
        team_a_standing.save()
        team_b_standing.save()

        # Swap fixtures
        for fixture_a, fixture_b in zip(team_a_fixtures, team_b_fixtures):
            if fixture_a.home_team == team_a:
                fixture_a.home_team = team_b
            elif fixture_a.away_team == team_a:
                fixture_a.away_team = team_b

            if fixture_b.home_team == team_b:
                fixture_b.home_team = team_a
            elif fixture_b.away_team == team_b:
                fixture_b.away_team = team_a

            fixture_a.save()
            fixture_b.save()

        return JsonResponse(status=200, data={'value': '{} swapped with {}'.format(team_a.name, team_b.name)})


class FixtureMakerView(FormView):
    form_class = FixtureCreator
    template_name = 'base_form.html'

    def form_valid(self, form):
        num_teams = form.cleaned_data['number_of_teams']
        times_to_play = form.cleaned_data['times_to_play']
        fixtures = make_fixtures(num_teams, times_to_play)

        return render(self.request, 'forms/created_fixtures.html', {'fixtures': fixtures})
