# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0019_result_void_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='away_team_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='home_team_score',
            field=models.IntegerField(default=0),
        ),
    ]
