# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpaas', '0004_auto_20160311_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentmodel',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]