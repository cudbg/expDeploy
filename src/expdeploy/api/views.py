from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Experiment
from planout.ops.random import *

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

def generateTask(variables):
	for var in variables:
		if (var["type"] == "UniformChoice"):
			print(var);
			param = UniformChoice(choices=var["choices"], unit="helloWorld",salt="hi");
			print(param.simpleExecute())
	return "bleh"

def task(request):
	expId = request.GET.get('experimentId', '');
	usrId = request.GET.get('userId', '');
	taskName = request.GET.get('task', '');
	exps = Experiment.objects.filter(name=expId, researcher_id=usrId);

	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")

	j = json.loads(exps[0].data);
	tasks = j["tasks"];



	for task in tasks:
		if task["name"] == taskName:
			#print("FOUND TASK");
			#print(task["variables"])

			variables = task["variables"];
			#result = generateTask(variables);
			return HttpResponse(task["variables"])

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")