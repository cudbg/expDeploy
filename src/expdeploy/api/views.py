from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Experiment
from .models import Tasks

from planout.ops.random import *
from expdeploy.testapp.models import ExperimentFile
import importlib;


def log(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		print(body);

		n = body["experiment_name"];
		researchID = body["researcher_id"];

		find = Experiment.objects.filter(name=n, researcher_id=researchID);

		tasks = None;
		if len(find) == 0:
			e = Experiment(name=n, researcher_id=researchID);
			e.save();
			t = Tasks(name=body["task_name"],experiment=e);
			t.save();
			tasks = t;
		else:
			e = find[0];
			findTask = Tasks.objects.filter(name=body["task_name"],experiment=e);
			if len(findTask) == 0:
				t = Tasks(name=body["task_name"],experiment=e);
				t.save();
				tasks = t;
			else:
				tasks = findTask[0]

		d = json.loads(tasks.trials);
		d[len(d)] = body["data"];
		tasks.trials = json.dumps(d);
		tasks.save();
		print(tasks.trials);

		return HttpResponse("Your data has been logged.")
	return HttpResponse("Not a post request")

def experiment(request):
	expId = request.GET.get('experimentId', '');
	usrId = request.GET.get('userId', '');
	exps = Experiment.objects.filter(name=expId, researcher_id=usrId);
	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")
	else:
		print(exps)
		return HttpResponse(exps[0].data)

def task(request):
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	taskName = request.GET.get('task', '');
	wid = request.GET.get('wid', '');
	n = int(request.GET.get('n', '1'));

	exps = ExperimentFile.objects.filter(username=usrId);

	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")

	expsBackwards = reversed(exps);
	for exp in expsBackwards:
		if (exp.original_filename == (expId + ".py")):
			Task = getattr(importlib.import_module("expdeploy." + str(exp.docfile).strip().replace(".py","").replace("/",".")), taskName)
			params = []
			for i in range(0,n):
				exp = Task(userid=wid+str(i));
				params.append(exp.get_params())
			return HttpResponse('{"params":' + str(params) + "}")

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")