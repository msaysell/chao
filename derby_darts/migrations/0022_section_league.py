# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0021_auto_20151015_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='league',
            field=models.ForeignKey(to='derby_darts.League', null=True),
        ),
    ]
