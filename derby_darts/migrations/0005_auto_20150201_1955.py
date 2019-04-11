# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0004_auto_20150131_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.CharField(max_length=50, choices=[(b'summer', b'summer'), (b'winter', b'winter')])),
                ('year', models.IntegerField()),
                ('league', models.ForeignKey(to='derby_darts.League', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeasonStanding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.IntegerField()),
                ('season', models.ForeignKey(to='derby_darts.Season', on_delete=models.CASCADE)),
                ('team', models.ForeignKey(to='derby_darts.Team', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fixture',
            name='league',
        ),
        migrations.RemoveField(
            model_name='team',
            name='league_section',
        ),
        migrations.AddField(
            model_name='fixture',
            name='season',
            field=models.ForeignKey(to='derby_darts.Season', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
