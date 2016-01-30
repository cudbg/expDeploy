# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='attachments')),
                ('username', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]