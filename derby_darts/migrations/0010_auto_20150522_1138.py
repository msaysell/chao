# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0009_userprivileges'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=75)),
                ('content', models.CharField(max_length=400)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('league', models.ForeignKey(to='derby_darts.League', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterModelOptions(
            name='rule',
            options={'ordering': ['id']},
        ),
    ]
