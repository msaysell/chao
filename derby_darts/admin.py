from django.contrib import admin

# Register your models here.
from derby_darts.models import Team, UserPrivileges, League, Season, Competition, CompetitionFixture, Result, Section, \
    Player, Fixture, SeasonPointDeduction, SeasonStanding, UnprocessedMessage

from django.db.models import Q

admin.site.register(League)
admin.site.register(Competition)
admin.site.register(CompetitionFixture)
admin.site.register(Fixture)
admin.site.register(Team)
admin.site.register(Season)
admin.site.register(Section)
admin.site.register(UserPrivileges)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'get_fixture', 'home_team_score', 'away_team_score', 'season')
    list_filter = ('fixture__date', 'fixture__home_team', 'fixture__away_team')

    def get_fixture(self, obj):
        return obj.fixture

    def date(self, obj):
        _ = self
        return obj.fixture.date

    def season(self, obj):
        _ = self
        return obj.fixture.season.name

    get_fixture.admin_order_field = 'date'


class PlayerPhoneNumberFilter(admin.SimpleListFilter):
    title = "Has Phone Number"
    parameter_name = 'has_phone_number'

    def lookups(self, lookups, model_admin):
        return ('True', 'Yes'),

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(phone_number__isnull=False).exclude(Q(phone_number="-") | Q(phone_number=""))
        return queryset


class TeamFilter(admin.SimpleListFilter):
    title = "Team"
    parameter_name = "team"

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        return queryset.filter(team__league=request.league).order_by('team__name').distinct('team__name').values_list('team_id', 'team__name')

    def queryset(self, request, queryset):
        return queryset.filter(team__league=request.league)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'phone_number']
    list_filter = [TeamFilter, PlayerPhoneNumberFilter]


@admin.register(SeasonPointDeduction)
class DeductionAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(DeductionAdmin, self).get_form(request, obj, **kwargs)
        latest_season = Season.objects.filter(league=request.league).order_by('-start_date').first()
        form.base_fields['standing'].queryset = SeasonStanding.objects.filter(season=latest_season)

        return form

@admin.register(UnprocessedMessage)
class UnprocessedMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'text', 'date']
