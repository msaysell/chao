# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0011_userprivileges_can_create_wall_posts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasonstanding',
            options={'ordering': ['section']},
        ),
        migrations.AddField(
            model_name='league',
            name='short_url',
            field=models.CharField(max_length=20, unique=True, null=True, blank=True),
        ),
    ]
