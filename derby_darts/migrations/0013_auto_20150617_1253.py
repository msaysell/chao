# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0012_auto_20150608_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'League', max_length=50)),
                ('season', models.ForeignKey(to='derby_darts.Season')),
            ],
        ),
        migrations.AddField(
            model_name='fixture',
            name='competition',
            field=models.ForeignKey(blank=True, to='derby_darts.Competition', null=True),
        ),
    ]
