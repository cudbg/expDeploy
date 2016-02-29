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
	return os.path.join('testapp/templates/', filename)

class ExperimentModel(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	username = models.CharField(max_length=120, blank=True, null=True)

	def __str__(self):
		return str(self.name)

class ExperimentFile(models.Model):
	#original_filename stored as charfield.
	experiment = models.ForeignKey(ExperimentModel)
	#experimentname = models.CharField(max_length=120, blank=True, null=True)
	original_filename = models.CharField(max_length = 128)
	docfile = models.FileField(upload_to=uuid_file_name)
	username = models.CharField(max_length=120, blank=True, null=True)
	filetext = models.TextField()

	def __str__(self):
		return str(self.docfile)