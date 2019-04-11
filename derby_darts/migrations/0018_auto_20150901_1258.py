# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0017_auto_20150825_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='home_team',
            field=models.ForeignKey(related_name='home_team', blank=True, to='derby_darts.Team', null=True, on_delete=models.CASCADE),
        ),
    ]
