# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0002_auto_20150129_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamFixtureResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('fixture', models.ForeignKey(to='derby_darts.TeamFixture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='leaguestanding',
            name='games_played',
        ),
        migrations.RemoveField(
            model_name='teamfixture',
            name='away_team_score',
        ),
        migrations.RemoveField(
            model_name='teamfixture',
            name='home_team_score',
        ),
    ]
