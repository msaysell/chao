# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0005_auto_20150201_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='competition_name',
            field=models.CharField(default=b'League', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fixture',
            name='away_team',
            field=models.ForeignKey(related_name='away_team', to='derby_darts.Team', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='season',
            name='season',
            field=models.CharField(max_length=50, choices=[(b'Summer', b'Summer'), (b'Winter', b'Winter')]),
            preserve_default=True,
        ),
    ]
