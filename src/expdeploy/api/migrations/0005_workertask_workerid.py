# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='workertask',
            name='workerId',
            field=models.TextField(default=b''),
        ),
    ]
