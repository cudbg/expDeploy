from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from django.db import models

class ExperimentFile(models.Model):
	#can send html and static files to separate locations later
    docfile = models.FileField(upload_to='testapp/webfiles')
    username = models.CharField(max_length=120, blank=True, null=True)
    filename = models.CharField(max_length=120, blank=True, null=True)

    #def __str__(self):
    #	return self.docfile