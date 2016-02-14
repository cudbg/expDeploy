from django.db import models
from jsonfield import JSONField
import collections;


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    researcher_id = models.CharField(max_length=200)
    data = models.CharField(max_length=1000000,default="{}")


class Tasks (models.Model):
	trials = models.CharField(max_length=10000,default="{}")
	name = models.CharField(max_length=200)
	experiment = models.ForeignKey(Experiment);


