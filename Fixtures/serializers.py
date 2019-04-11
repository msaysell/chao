from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer
from derby_darts.models import Fixture, Team, Result, Season, SeasonStanding, Section


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"


class FixtureSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    result = ResultSerializer()

    class Meta:
        model = Fixture
        fields = "__all__"


class SectionSerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'id']
        model = Section