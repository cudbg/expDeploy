from django.db import models
from expdeploy.gpaas.models import ExperimentFile
from expdeploy.gpaas.models import ExperimentModel

from jsonfield import JSONField
import collections;


class WorkerTask (models.Model):


	hitId = models.TextField(default="none")
	assignmentId = models.TextField(default="")
	workerId = models.TextField(default="")
	params = models.TextField(default="{}")
	results = models.TextField(default='{"data":[], "metadata":[]}')
	history = models.TextField(default='{"events":[] }')
	experiment = models.ForeignKey(ExperimentModel)
	params = models.TextField(default="PaidAssignment")#PaidAssignment, QualificationTask, TrainingTask
	metaData = models.ForeignKey('Metadata',default="",null=True,blank=True)

	currentStatus = models.CharField(max_length=100, default="Waiting")
	paid = models.BooleanField(default=False)
	isSandbox = models.BooleanField(default=True)
	researcher = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	wid = models.CharField(max_length=200)
	identifier = models.CharField(max_length=200)

	

class HistoryEvent (models.Model):

	workerTask = models.ForeignKey('WorkerTask',default=0,null=True,blank=True)
	newStatus = models.TextField(default="")
	eventType = models.TextField(default="changeStatus")
	timeStamp = models.IntegerField(default=0)



class Metadata (models.Model):

	userAgent = models.TextField(default="")
	dimensions = models.TextField(default="")
	start = models.IntegerField(default=0)
	end = models.IntegerField(default=0)