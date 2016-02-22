# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 05:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20160209_0611'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trials', models.CharField(default=b'{}', max_length=10000)),
                ('name', models.CharField(max_length=200)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Experiment')),
            ],
        ),
    ]