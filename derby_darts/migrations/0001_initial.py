# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerFixture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
                ('away_player', models.ForeignKey(related_name='away_player', to=settings.AUTH_USER_MODEL)),
                ('competition', models.ForeignKey(to='derby_darts.Competition')),
                ('home_player', models.ForeignKey(related_name='home_player', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_180s', models.IntegerField(default=0)),
                ('num_140s', models.IntegerField(default=0)),
                ('num_100s', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamFixture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('away_team', models.ForeignKey(related_name='away_team', to='derby_darts.Team')),
                ('competition', models.ForeignKey(to='derby_darts.Competition')),
                ('home_team', models.ForeignKey(related_name='home_team', to='derby_darts.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='playerprofile',
            name='team',
            field=models.ForeignKey(to='derby_darts.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
