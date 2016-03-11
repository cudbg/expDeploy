# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpaas', '0002_auto_20160311_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentmodel',
            name='n',
            field=models.IntegerField(null=5),
        ),
        migrations.AddField(
            model_name='experimentmodel',
            name='sandbox',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='experimentmodel',
            name='hit_payment',
            field=models.FloatField(blank=0.1),
        ),
    ]
