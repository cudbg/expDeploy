# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 03:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workertask',
            name='researcher',
            field=models.CharField(default=datetime.datetime(2016, 2, 22, 3, 18, 8, 908040, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
