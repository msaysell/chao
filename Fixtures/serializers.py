from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer
from derby_darts.models import Fixture, Team, Result, Season, SeasonStanding, Section


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team


class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result


class FixtureSerializer(ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    result = ResultSerializer()

    class Meta:
        model = Fixture


class SectionSerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'id']
        model = Section