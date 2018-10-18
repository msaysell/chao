# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_sections_for_standings(apps, schema_editor):
    SeasonStanding = apps.get_model('derby_darts', 'SeasonStanding')
    Section = apps.get_model('derby_darts', 'Section')

    for standing in SeasonStanding.objects.all():
        number = standing.section
        section, created = Section.objects.get_or_create(league=standing.season.league, name=str(number), order=number)
        standing.season_section = section
        standing.save()


def reverse_migration(apps, schema_editor):
    SeasonStanding = apps.get_model('derby_darts', 'SeasonStanding')
    # Section = apps.get_model('derby_darts', 'Section')

    for standing in SeasonStanding.objects.all():
        standing.section = standing.season_section.order
        standing.save()


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0022_section_league'),
    ]

    operations = [
        migrations.RunPython(create_sections_for_standings, reverse_migration),
    ]
