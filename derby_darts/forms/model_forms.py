from datetime import datetime
from django.forms import ModelForm, Textarea
from derby_darts.models import Team, PlayerProfile, Fixture, Result, League, Season, WallPost, Competition, \
    CompetitionFixture, Rule, RuleCategory, SeasonPointDeduction
from djng.forms import NgModelFormMixin, NgModelForm
from djng.styling.bootstrap3.forms import Bootstrap3ModelForm

__author__ = 'michael.saysell'


class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LeagueForm(BootstrapModelForm):
    class Meta:
        model = League
        fields = '__all__'


class SeasonForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter a name for this season'})
        self.fields['start_date'].widget.attrs.update({'placeholder': 'Please select a start date',
                                                       'id': 'datepicker'})

    class Meta:
        model = Season
        exclude = ['season', 'year']


class TeamForm(BootstrapModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerForm(BootstrapModelForm):
    class Meta:
        model = PlayerProfile
        fields = '__all__'


class CompetitionForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CompetitionForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields["season"].queryset = Season.objects.filter(league=self.request.league)

    class Meta:
        model = Competition
        fields = '__all__'


class DeductionForm(ModelForm):
    class Meta:
        model = SeasonPointDeduction
        fields = '__all__'


class FixtureForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(FixtureForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'placeholder': 'Please select a date', 'id': 'datepicker'})
        if self.request:
            self.fields["season"].queryset = Season.objects.filter(league=self.request.league)
            self.fields["home_team"].queryset = Team.objects.filter(league=self.request.league)
            self.fields["away_team"].queryset = Team.objects.filter(league=self.request.league)

    class Meta:
        model = Fixture
        fields = '__all__'


class CompetitionFixtureForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CompetitionFixtureForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'placeholder': 'Please select a date', 'id': 'datepicker'})
        if self.request:
            self.fields["season"].queryset = Season.objects.filter(league=self.request.league)
            self.fields["competition"].queryset = Competition.objects.filter(season__league=self.request.league)
            # self.fields["away_team"].queryset = Team.objects.filter(league=self.request.league)

    class Meta:
        model = CompetitionFixture
        exclude = ['home_team', 'away_team']


class ResultForm(NgModelFormMixin, Bootstrap3ModelForm):
    form_name = 'results_form'
    scope_prefix = 'result'

    def __init__(self, *args, **kwargs):
        self.league = kwargs.pop('league')
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['fixture'].queryset = Fixture.objects.filter(season__league=self.league,
                                                                 home_team__isnull=False,
                                                                 competitionfixture__isnull=True,
                                                                 result__isnull=True,
                                                                 date__lte=datetime.now())

    class Meta:
        model = Result
        fields = '__all__'


class WallPostForm(BootstrapModelForm):
    class Meta:
        model = WallPost
        fields = '__all__'
        widgets = {'content': Textarea(attrs={"class": "form-control"})}
        exclude = ['date_created', 'league']


class RuleForm(BootstrapModelForm):
    class Meta:
        model = Rule
        fields = '__all__'
        widgets = {'content': Textarea(attrs={"class": "form-control"})}


class RuleCategoryForm(BootstrapModelForm):
    class Meta:
        model = RuleCategory
        fields = '__all__'
        widgets = {'content': Textarea(attrs={"class": "form-control"})}
