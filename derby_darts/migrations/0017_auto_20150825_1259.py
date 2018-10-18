# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0016_competitionfixture_competition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rulecategory',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='rule',
            name='description',
            field=models.CharField(max_length=400),
        ),
    ]
