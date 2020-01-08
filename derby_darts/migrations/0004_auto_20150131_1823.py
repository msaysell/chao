# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0003_auto_20150130_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('away_team', models.ForeignKey(related_name='away_team', to='derby_darts.Team', on_delete=models.CASCADE)),
                ('home_team', models.ForeignKey(related_name='home_team', to='derby_darts.Team', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('fixture', models.OneToOneField(to='derby_darts.Fixture', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('league', models.ForeignKey(to='derby_darts.League', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='leaguestanding',
            name='team',
        ),
        migrations.DeleteModel(
            name='LeagueStanding',
        ),
        migrations.RemoveField(
            model_name='playerfixture',
            name='away_player',
        ),
        migrations.RemoveField(
            model_name='playerfixture',
            name='competition',
        ),
        migrations.RemoveField(
            model_name='playerfixture',
            name='home_player',
        ),
        migrations.DeleteModel(
            name='PlayerFixture',
        ),
        migrations.RemoveField(
            model_name='teamfixture',
            name='away_team',
        ),
        migrations.RemoveField(
            model_name='teamfixture',
            name='competition',
        ),
        migrations.DeleteModel(
            name='Competition',
        ),
        migrations.RemoveField(
            model_name='teamfixture',
            name='home_team',
        ),
        migrations.RemoveField(
            model_name='teamfixtureresult',
            name='fixture',
        ),
        migrations.DeleteModel(
            name='TeamFixture',
        ),
        migrations.DeleteModel(
            name='TeamFixtureResult',
        ),
        migrations.AddField(
            model_name='fixture',
            name='league',
            field=models.ForeignKey(to='derby_darts.League', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='league',
            field=models.ForeignKey(to='derby_darts.League', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='league_section',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
