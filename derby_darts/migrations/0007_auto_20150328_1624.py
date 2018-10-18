# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0006_auto_20150328_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='away_team',
            field=models.ForeignKey(related_name='away_team', blank=True, to='derby_darts.Team', null=True),
            preserve_default=True,
        ),
    ]
