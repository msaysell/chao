# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0010_auto_20150522_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprivileges',
            name='can_create_wall_posts',
            field=models.BooleanField(default=False),
        ),
    ]
