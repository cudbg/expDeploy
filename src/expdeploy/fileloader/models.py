
# -*- coding: utf-8 -*-
from django.db import models

class TemplateFile(models.Model):
    docfile = models.FileField(upload_to='documents')