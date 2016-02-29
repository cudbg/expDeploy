from django.db import models
from expdeploy.testapp.models import ExperimentFile
from expdeploy.testapp.models import ExperimentModel

from jsonfield import JSONField
import collections;


class WorkerTask (models.Model):
	params = models.TextField(default="{}")
	results = models.TextField(default="null")
	experiment = models.ForeignKey(ExperimentModel)


	researcher = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	wid = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200)



