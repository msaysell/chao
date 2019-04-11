from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save


class League(models.Model):
    name = models.CharField(max_length=100)
    short_url = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=50)
    league = models.ForeignKey(League, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('derby_darts:team_details', kwargs={'pk': self.pk})


class Player(models.Model):
    team = models.ForeignKey(Team, null=True, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='')
    is_county = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=24, null=True, blank=True)

    class Meta:
        ordering = ['-is_county', 'name']


class Season(models.Model):
    def __str__(self):
        return self.get_name()

    WINTER = 'Winter'
    SUMMER = 'Summer'

    SEASONAL_CHOICES = ((SUMMER, SUMMER),
                        (WINTER, WINTER))

    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season = models.CharField(max_length=50, choices=SEASONAL_CHOICES, null=True)
    year = models.IntegerField(null=True)
    name = models.CharField(max_length=30, null=True)
    start_date = models.DateField(default=None, null=True)

    def get_name(self):
        if self.name:
            return self.name

        # Support for older leagues
        return '{} {}'.format(self.season, self.year)


class Section(models.Model):
    class Meta:
        ordering = ['order']
    league = models.ForeignKey(League, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    order = models.IntegerField()


class SeasonStanding(models.Model):
    class Meta:
        ordering = ['section']

    def __str__(self):
        return 'Standing for {}'.format(self.team.name)

    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season_section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    section = models.IntegerField()


class SeasonPointDeduction(models.Model):
    standing = models.ForeignKey(SeasonStanding, on_delete=models.CASCADE)
    reason = models.CharField(max_length=128, null=True, blank=True)
    num_of_points = models.SmallIntegerField(default=0)


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='player_profiles', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=24, null=True, blank=True)
    num_100s = models.IntegerField(default=0)
    num_140s = models.IntegerField(default=0)
    num_180s = models.IntegerField(default=0)

    def __str__(self):
        return '{}\'s profile'.format(self.user.get_full_name())


class Competition(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='League')

    def __str__(self):
        return self.name


class Fixture(models.Model):
    date = models.DateField()
    season = models.ForeignKey(Season, null=True, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_team', null=True, blank=True, on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} v {1}".format(self.get_home_team_name(), self.get_away_team_name())

    def get_home_team_name(self):

        if not self.home_team:
            if isinstance(self, CompetitionFixture):
                return self.competitionfixture.get_home_team_name()
            return ''
        return self.home_team.name

    def get_away_team_name(self):
        if not self.away_team:
            if isinstance(self, CompetitionFixture):
                return self.competitionfixture.get_away_team_name()
            return ''
        return self.away_team.name


class CompetitionFixture(Fixture):
    competition = models.ForeignKey(Competition, null=True, on_delete=models.CASCADE)

    def get_home_team_name(self):
        if not self.home_team:
            return self.competition.name
        return self.home_team

    def get_away_team_name(self):
        if not self.away_team:
            return self.competition.name
        return self.away_team.name


class Result(models.Model):
    def __str__(self):
        return 'Result added for {}'.format(self.fixture)

    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE)
    home_team_score = models.IntegerField(default=0, blank=False)
    away_team_score = models.IntegerField(default=0, blank=False)
    void_result = models.BooleanField(default=False)


class RuleCategory(models.Model):
    name = models.CharField(max_length=250)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class Rule(models.Model):
    category = models.ForeignKey(RuleCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=400)

    class Meta:
        ordering = ['id']


class UserPrivileges(models.Model):
    user = models.OneToOneField(User, related_name='privileges', on_delete=models.CASCADE)
    can_modify_rules = models.BooleanField(default=False)
    can_create_wall_posts = models.BooleanField(default=False)


def create_user_privileges(sender, instance, created, **kwargs):
    if created:
        UserPrivileges.objects.create(user=instance)

post_save.connect(create_user_privileges, sender=User)


class WallPost(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    content = models.CharField(max_length=4000)
    date_created = models.DateTimeField(auto_now=True)


class UnprocessedMessage(models.Model):
    text = models.CharField(max_length=1024, null=True, blank=True)
    sender = models.CharField(max_length=24, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    has_processed = models.BooleanField(default=False, blank=True)
