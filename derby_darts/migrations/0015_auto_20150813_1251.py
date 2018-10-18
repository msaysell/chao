# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0014_auto_20150803_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionFixture',
            fields=[
                ('fixture_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='derby_darts.Fixture')),
            ],
            bases=('derby_darts.fixture',),
        ),
        migrations.RemoveField(
            model_name='fixture',
            name='competition',
        ),
        migrations.RemoveField(
            model_name='fixture',
            name='competition_name',
        ),
        migrations.AlterField(
            model_name='season',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
