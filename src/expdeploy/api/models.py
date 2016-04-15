from django.db import models
from expdeploy.gpaas.models import ExperimentFile
from expdeploy.gpaas.models import ExperimentModel

from jsonfield import JSONField
import collections;


class WorkerTask (models.Model):

	params = models.TextField(default="{}")
	results = models.TextField(default='{"data":[], "metadata":[]}')
	history = models.TextField(default='{"events":[] }')
	experiment = models.ForeignKey(ExperimentModel)

	currentStatus = models.CharField(max_length=100, default="Waiting")
	paid = models.BooleanField(default=False)

	researcher = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	wid = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200)



