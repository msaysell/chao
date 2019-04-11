# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0015_auto_20150813_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitionfixture',
            name='competition',
            field=models.ForeignKey(to='derby_darts.Competition', null=True, on_delete=models.CASCADE),
        ),
    ]
