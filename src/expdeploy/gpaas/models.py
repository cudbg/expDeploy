from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from django.db import models
from uuid import uuid4
import os

#arbitrary name generating function
from django.contrib.auth.models import User


class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aws_key_id = models.CharField(max_length=250)
    aws_secret_key = models.CharField(max_length=250)

def uuid_file_name(instance, filename):
	instance.filename = filename
	filetype = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid4()), filetype)
	return os.path.join('gpaas/templates/', filename)

class ExperimentModel(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	username = models.CharField(max_length=120, blank=True, null=True)
	hit_description = models.CharField(max_length=120)
	hit_payment = models.FloatField(blank=0.1)
	hit_keywords = models.CharField(max_length=120)
	sandbox = models.BooleanField(default=True)
	n = models.IntegerField(default=5);


	def __str__(self):
		return str(self.name)

class ExperimentFile(models.Model):
	docfile = models.FileField(upload_to=uuid_file_name)
	experiment = models.ForeignKey(ExperimentModel)
	filetext = models.TextField()
	original_filename = models.CharField(max_length = 128)
	username = models.CharField(max_length=120, blank=True, null=True)
	

	def __str__(self):
		return str(self.docfile)