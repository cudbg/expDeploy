# -*- coding: utf-8 -*-
from django.db import models

class Image(models.Model):
    imgfile = models.ImageField(upload_to='images', blank=True, null=True)
