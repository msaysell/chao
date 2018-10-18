# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0013_auto_20150617_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='name',
            field=models.CharField(default=b'Season', max_length=30),
        ),
        migrations.AddField(
            model_name='season',
            name='start_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='season',
            field=models.CharField(max_length=50, null=True, choices=[(b'Summer', b'Summer'), (b'Winter', b'Winter')]),
        ),
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
