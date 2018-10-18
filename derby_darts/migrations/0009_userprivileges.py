# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('derby_darts', '0008_auto_20150419_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPrivileges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('can_modify_rules', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='privileges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
