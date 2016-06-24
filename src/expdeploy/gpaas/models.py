# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import os
from django.contrib.auth.models import User
from uuid import uuid4

# function used in ExperimentFile model to create alias
def uuid_file_name(instance, filename):
	instance.filename = filename
	filetype = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid4()), filetype)
	return os.path.join('gpaas/experimentfiles/', filename)

class ExperimentModel(models.Model):
	name = models.CharField(max_length=120, blank=True, null=True)
	username = models.CharField(max_length=120, blank=True, null=True)
	hit_description = models.CharField(max_length=120)
	per_task_payment = models.FloatField(blank=0.1)
	bonus_payment = models.FloatField(blank=0)
	hit_keywords = models.CharField(max_length=120)
	sandbox = models.BooleanField(default=True)
	n = models.IntegerField(default=5);
	published_mturk = models.BooleanField(default=False);
	published_sandbox = models.BooleanField(default=False);	
	banned = models.TextField(default='{"ids":[]}')
	hitID = models.CharField(max_length=120)
	config_file = models.CharField(max_length=120,default="config.json")

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

class QualificationsModel(models.Model):
	adult_requirement = models.BooleanField(default=True) # adults only
	experiment = models.ForeignKey(ExperimentModel)
	percentage_hits_approved = models.IntegerField(default=95)
	percentage_assignments_submitted = models.IntegerField(default=95)
	username = models.CharField(max_length=120, blank=True, null=True)

	def __str__(self):
		return str(self.experiment)

class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aws_key_id = models.CharField(max_length=250)
    aws_secret_key = models.CharField(max_length=250)