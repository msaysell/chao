# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueStanding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('games_played', models.IntegerField()),
                ('points', models.IntegerField()),
                ('team', models.ForeignKey(to='derby_darts.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='competition',
            name='name',
            field=models.CharField(max_length=70, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='sport',
            field=models.CharField(max_length=30, null=True),
            preserve_default=True,
        ),
    ]
