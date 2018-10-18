# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0023_auto_20151015_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='content',
            field=models.CharField(max_length=4000),
        ),
    ]
