from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from django.db import models

class ExperimentFile(models.Model):
    docfile = models.FileField(upload_to='attachments')
    username = models.CharField(max_length=120, blank=True, null=True)