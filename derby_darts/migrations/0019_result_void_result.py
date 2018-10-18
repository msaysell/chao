# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0018_auto_20150901_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='void_result',
            field=models.BooleanField(default=False),
        ),
    ]
