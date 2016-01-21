# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageloader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imgfile',
            field=models.ImageField(null=True, upload_to=b'images', blank=True),
        ),
    ]
