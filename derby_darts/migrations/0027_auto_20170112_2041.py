# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-12 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('derby_darts', '0026_auto_20170108_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnprocessedMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=1024, null=True)),
                ('sender', models.CharField(blank=True, max_length=24, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('has_processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='playerprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]