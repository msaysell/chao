import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, View, DetailView

from derby_darts.forms.forms import ContactForm, AddPlayerForm
from derby_darts.forms.model_forms import TeamForm, PlayerForm, FixtureForm, LeagueForm, WallPostForm, CompetitionForm, \
    CompetitionFixtureForm
from .forms import model_forms
from .models import Team, Season, SeasonStanding, Fixture, WallPost, Player, Result, UnprocessedMessage
from markdown_deux import markdown


def user_can_edit(user):
    return not user.is_anonymous() and user.privileges.can_create_wall_posts


@csrf_exempt
def ping(request):
    return JsonResponse(data={'valid': True})


@csrf_exempt
def validate_number(request):
    number = request.POST.get('phoneNumber', None)
    team_name = request.POST.get('teamName', None)

    if number is None or team_name is None:
        return JsonResponse(data={'message': 'Team name or number missing'}, status=401)

    return JsonResponse(data={'valid': Player.objects.filter(phone_number=number,
                                                             team__name=team_name).exists()})


class TeamListView(ListView):
    model = Team
    context_object_name = 'team_list'
    template_name = 'team_list.html'

    def get_queryset(self):
        current_season = Season.objects.filter(league=self.request.league).order_by('-start_date').first()
        return Team.objects.filter(league=self.request.league, seasonstanding__season=current_season).order_by('name')


class TeamDetailView(DetailView):
    model = Team
    context_object_name = 'team'
    template_name = 'team_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['can_edit'] = user_can_edit(self.request.user)
        return context


class AddPlayerView(LoginRequiredMixin, FormView):
    form_class = AddPlayerForm
    template_name = 'base_form.html'

    def form_valid(self, form):
        team_id = self.kwargs.get('pk')
        team = Team.objects.get(pk=team_id)

        players = form.cleaned_data.get('players', '').splitlines()

        for player in players:
            Player.objects.get_or_create(team=team, name=player.lstrip('@'), is_county='@' in player)

        return HttpResponseRedirect(team.get_absolute_url())


class PostListView(ListView):
    model = WallPost
    paginate_by = 10
    template_name = 'home.html'

    def get_queryset(self):
        return self.model.objects.filter(league=self.request.league).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        can_edit = not self.request.user.is_anonymous() and self.request.user.privileges.can_create_wall_posts
        if can_edit:
            context['can_edit'] = True
            context['new_form'] = WallPostForm()
        return context


class PostFormView(UserPassesTestMixin, View):

    def post(self, request):
        form = WallPostForm(request.POST)
        if form.is_valid():
            wall_post = form.save(commit=False)
            wall_post.league = request.league
            wall_post.save()
            return JsonResponse({'success': True,
                                 'title': form.cleaned_data['title'],
                                 'description': markdown(form.cleaned_data['content'], "default")})
        return JsonResponse(status=400, data={})

    def test_func(self):
        return user_can_edit(self.request.user)


def index(request):

    can_edit = not request.user.is_anonymous() and request.user.privileges.can_create_wall_posts

    if request.method == 'POST' and can_edit:
        returned_form = WallPostForm(request.POST)
        if returned_form.is_valid():
            wall_post = returned_form.save(commit=False)
            wall_post.league = request.league
            wall_post.save()

            return JsonResponse({"success": True,
                                 "message": "{0} added".format(str(returned_form.instance)),
                                 "title": wall_post.title,
                                 "description": markdown(wall_post.content, "default")},
                                status=200)
        else:
            return JsonResponse({"success": False,
                                 "message": "invalid"},
                                status=400)

    form = None
    if can_edit:
        form = WallPostForm()

    return render(request,
                  'home.html',
                  {'can_edit': can_edit,
                   'new_form': form,
                   'posts': WallPost.objects.filter(league=request.league).order_by('-id')})


@login_required
def get_edit_post_form(request, post_id):
    post = WallPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = WallPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data={'id': post_id,
                                                  'title': form.cleaned_data['title'],
                                                  'description': markdown(form.cleaned_data['content'])})
        return JsonResponse(status=101, data={})
    return HttpResponse(WallPostForm(instance=post))


@login_required
def delete_post(request, post_id):
    post = WallPost.objects.get(id=post_id)

    if post.league != request.league:
        return JsonResponse(status=101, data={})

    post.delete()

    return JsonResponse(status=200, data={})


def league(request):

    current_season = Season.objects.filter(league=request.league).order_by('-start_date').first()

    return __render_league__(request, current_season)


def selected_league(request, season_id):
    season = Season.objects.get(league=request.league, id=season_id)
    return __render_league__(request, season)


def __render_league__(request, season):
    seasons = Season.objects.filter(league=request.league)

    return render(request, 'league.html', {'teams': Team.objects.filter(league=request.league),
                                           'current_season': season,
                                           'all_seasons': seasons})


def login_user(request):
    logout(request)  # Only needed to handle users that come to login page by url when logged in
    notification = None

    if request.POST:
        username = request.POST['username'].strip()
        password = request.POST['password']

        user = authenticate(username=username,
                            password=password)

        if user is None:
            notification = ("error", "The username and password you have provided is incorrect.")

        if user is not None and user.is_active is not None:
            notification = ("warning", "This account has been disabled. Please contact support.")

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("derby_darts:home"))

    return render(request,
                  'registration/login.html',
                  {
                      'form': AuthenticationForm(),
                      'notification': notification
                  })


@login_required
def new_team(request):
    return render_form(request, 'New Team', TeamForm())


@login_required
def new_league(request):
    return render_form(request, 'New League', LeagueForm())


@login_required
def new_player(request):
    return render_form(request, 'New Player', PlayerForm())


@login_required
def new_fixture(request):
    return render_form(request, 'New Fixture', FixtureForm(request=request))


@login_required
def new_competition_fixture(request):
    return render_form(request, 'New Competition Fixture', CompetitionFixtureForm(request=request))


@login_required
def new_competition(request):
    return render_form(request, 'New Competition', CompetitionForm(request=request))


@login_required
def new_result(request):
    result_form = model_forms.ResultForm()
    result_form.fields['fixture'].queryset = Fixture.objects.filter(season__league=request.league,
                                                                    competition__is_null=True,
                                                                    result__isnull=True,
                                                                    date__lte=datetime.date.today())

    return render_form(request, 'New Result', result_form)


class ResultFormView(FormView):
    form_class = model_forms.ResultForm
    template_name = 'forms/result_form.html'

    def get_context_data(self, **kwargs):
        context = super(ResultFormView, self).get_context_data(**kwargs)
        context['form_title'] = 'New Result'
        return context

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        form = self.form_class(data=data, league=request.league)
        if form.is_valid():
                return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(ResultFormView, self).get_form_kwargs()
        kwargs['league'] = self.request.league

        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse(status=200,
                            data={"message": "{0} added".format(str(form.instance))})

    def form_invalid(self, form):
        return JsonResponse(status=400, data={"message": 'Oops!'})


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'html_form.html'
    success_url = '/contact'

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        context['form_title'] = 'Contact Us'
        return context

    def form_valid(self, form):
        form.send_email()
        return super(ContactFormView, self).form_valid(form)


@login_required
def new_season(request):
    return render_form(request, 'New Season', model_forms.SeasonForm())


def render_form(request, form_title, form):

    if request.method == 'POST':
        returned_form = type(form)(request.POST)
        if returned_form.is_valid():
            returned_form.save()
            return JsonResponse({"success": True,
                                 "message": "{0} added".format(str(returned_form.instance))},
                                status=200)
        else:
            return JsonResponse({"success": False,
                                 "message": "invalid"},
                                status=400)

    return render(request,
                  'base_form.html',
                  {
                      'form_title': form_title,
                      'form': form
                  })


@login_required
def set_standings(request):
    request_league = request.league
    seasons = Season.objects.filter(league=request_league)

    return render(request, 'set_standings.html', {'teams': Team.objects.filter(league=request_league),
                                                  'seasons': seasons})


@login_required
def post_standings(request):
    if not request.POST:
        return Http404()
    team_list = json.loads(request.POST['json_data'])
    season = Season.objects.get(league=request.league,
                                id=request.POST['season'])

    for team_dict in team_list:
        team_name = team_dict['team_name']
        section = team_dict['section']

        team = Team.objects.get(league=request.league,
                                name=team_name)

        existing = SeasonStanding.objects.filter(season=season, team=team)

        if existing:
            if existing[0].section != section:
                existing[0].section = section
                existing[0].save()
                print('Standing for {} updated'.format(team_name))
        else:
            standing = SeasonStanding(season=season,
                                      team=team,
                                      section=section)
            standing.save()
            print('Standing added for {}'.format(team_name))

    return JsonResponse(status=200, data={})


class ReceiveMsgView(View):

    def handle_invalid_msg_format(self, from_number, text, date):
        prsd_date = datetime.datetime.strptime(date[:-5], "%Y-%m-%dT%H:%M:%S")

        msg = UnprocessedMessage.objects.create(text=text, date=prsd_date, sender=from_number)

        player = Player.objects.filter(phone_number=from_number).first()

        msg = '{}: {}'.format(player.team.name if player else from_number, text)
        send_mail(subject='Invalid Result Text Message',
                  message=msg,
                  from_email='darts@leaguecity.uk',
                  recipient_list=['mike@saysell.net'],
                  fail_silently=True)

        return JsonResponse(status=200, data={'message': msg})

    def get(self, request):
        return JsonResponse(status=200, data={})

    def post(self, request):
        from_number = request.POST.get('sender')
        text = request.POST.get('text', '')
        date = request.POST.get('messageTime')

        msg = '{}: {}'.format(from_number, text)

        if not text or from_number is None:
            return self.handle_invalid_msg_format(from_number, text, date)

        players = Player.objects.filter(phone_number=from_number).only('team')
        if not players.exists():
            return self.handle_invalid_msg_format(from_number, text, date)

        team = players.first().team

        missing_result_fixtures = Fixture.objects.filter(Q(home_team=team) | Q(away_team=team),
                                                         date__lte=datetime.datetime.now(),
                                                         date__gte=datetime.datetime.now() - datetime.timedelta(days=7),
                                                         season__league=request.league,
                                                         result__isnull=True)

        if not missing_result_fixtures.exists():
            return self.handle_invalid_msg_format(from_number, text, date)

        parsed_msg = text.strip('"').replace('-', ' ').split()

        if len(parsed_msg) < 3:
            return self.handle_invalid_msg_format(from_number, text, date)

        result = parsed_msg[0].lower()
        if result == 'won':
            team_won = True
        elif result == 'lost':
            team_won = False
        else:
            return self.handle_invalid_msg_format(from_number, text, date)

        if not parsed_msg[1].isdigit() or not parsed_msg[2].isdigit():
            return self.handle_invalid_msg_format(from_number, text, date)

        winning_score = parsed_msg[1]
        losing_score = parsed_msg[2]
        if int(parsed_msg[1]) < int(parsed_msg[2]):
            temp = winning_score
            winning_score = losing_score
            losing_score = temp

        latest_fixture = missing_result_fixtures.order_by('-date').first()
        result_dict = {'fixture': latest_fixture}

        is_home_team = latest_fixture.home_team == team
        if team_won:
            if is_home_team:
                result_dict['home_team_score'] = winning_score
                result_dict['away_team_score'] = losing_score
            else:
                result_dict['home_team_score'] = losing_score
                result_dict['away_team_score'] = winning_score
        else:
            if is_home_team:
                result_dict['home_team_score'] = losing_score
                result_dict['away_team_score'] = winning_score
            else:
                result_dict['home_team_score'] = winning_score
                result_dict['away_team_score'] = losing_score

        result = Result.objects.create(**result_dict)

        return JsonResponse(status=200, data={'message': str(result)})
