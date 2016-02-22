from django.db import models
from expdeploy.testapp.models import ExperimentFile

from jsonfield import JSONField
import collections;


class WorkerTask (models.Model):
	params = models.CharField(max_length=10000,default="{}")
	results = models.CharField(max_length=10000,default="{}")
	experiment = models.CharField(max_length=10000,default="{}")

	researcher = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	wid = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200)



