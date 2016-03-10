from django.shortcuts import render
from django.http import HttpResponse
import json
#from .models import Experiment
from .models import WorkerTask

from planout.ops.random import *
from expdeploy.gpaas.models import ExperimentFile
from expdeploy.gpaas.models import Researcher

import importlib;
import random
import string
import boto.mturk.connection
 



def mturk(request):
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	
	researcher = Researcher.objects.filter(user__username=usrId)[0];
	key = researcher.aws_key_id;
	secret_key = researcher.aws_secret_key;
	sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
	real_host = 'mechanicalturk.amazonaws.com'
	
	mturk = boto.mturk.connection.MTurkConnection(
	    aws_access_key_id = key,
	    aws_secret_access_key = secret_key,
	    host = sandbox_host,
	    debug = 1 # debug = 2 prints out all requests.
	)
	 
	print boto.Version 
	print mturk.get_account_balance() 


	url = "https://www.yahoo.com"
	title = expId
	description = "The more verbose description of the job!"
	keywords = ["cats", "dogs", "rabbits"]
	frame_height = 500 # the height of the iframe holding the external hit
	amount = .05
	 
	questionform = boto.mturk.question.ExternalQuestion( url, frame_height )
	 
	create_hit_result = mturk.create_hit(
	    title = title,
	    description = description,
	    keywords = keywords,
	    question = questionform,
	    reward = boto.mturk.price.Price( amount = amount),
	    response_groups = ( 'Minimal', 'HITDetail' ), # I don't know what response groups are
	)
	return HttpResponse("Successfully posted to MTurk");



def result(request):
	expId = request.GET.get('experiment', '');
	taskname = request.GET.get('task', '');
	usrId = request.GET.get('researcher', '');
	print(usrId)
	#TODO: Filter by experiment name
	find_tasks = WorkerTask.objects.filter(experiment__name=expId,name=taskname, researcher=usrId);

	data = []
	for task in find_tasks:
		print("SSS" + task.experiment.name)
		d = byteify(json.loads(task.results));
		data.append(d);
	print(data);
	return HttpResponse(data)

def log(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		#print(body["task_id"]);

		#TODO: Filter by experiment name

		find_tasks = WorkerTask.objects.filter( wid=body["worker_id"],name=body["task_name"],identifier=body["task_id"]);
		print(find_tasks);

		task = find_tasks[0]

		if (task.results == "null"):
			task.results = "{}";

		d = json.loads(task.results)
		d[len(d)] = body["data"];

		task.results = json.dumps(d);
		task.save()



		#find_tasks = WorkerTask.objects.filter(name=body["task_name"], wid=body["worker_id"], experiment=body["experiment_name"]);

		return HttpResponse(str(d));

	# 	n = body["experiment_name"];
	# 	researchID = body["researcher_id"];

	# 	find = Experiment.objects.filter(name=n, researcher_id=researchID);

	# 	tasks = None;
	# 	if len(find) == 0:
	# 		e = Experiment(name=n, researcher_id=researchID);
	# 		e.save();
	# 		t = Tasks(name=body["task_name"],experiment=e);
	# 		t.save();
	# 		tasks = t;
	# 	else:
	# 		e = find[0];
	# 		findTask = Tasks.objects.filter(name=body["task_name"],experiment=e);
	# 		if len(findTask) == 0:
	# 			t = Tasks(name=body["task_name"],experiment=e);
	# 			t.save();
	# 			tasks = t;
	# 		else:
	# 			tasks = findTask[0]

	# 	d = json.loads(tasks.trials);
	# 	d[len(d)] = body["data"];
	# 	tasks.trials = json.dumps(d);
	# 	tasks.save();
	# 	print(tasks.trials);

	# 	return HttpResponse("Your data has been logged.")
	# return HttpResponse("Not a post request")

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
	print("test 1");

	exps = ExperimentFile.objects.filter(username=usrId);
	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")

	expsBackwards = reversed(exps);
	for exp in expsBackwards:
		if (exp.original_filename == (expId + ".py")):
			print("test 2");

			EX = exp.experiment
			print("n2222"+EX.name);
			
			return_tasks = []
			find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment=EX);
			print(find_tasks);
			if (len(find_tasks) == 0):
				Task = getattr(importlib.import_module("expdeploy." + str(exp.docfile).strip().replace(".py","").replace("/",".")), taskName)
			
				print("Creating new tasks right now");
				
				for i in range(0,n):
					exp = Task(userid=wid+str(i));

					task_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

					NewTask = WorkerTask(name=taskName, wid=wid, experiment=EX, identifier=task_id, researcher=usrId)
					param = exp.get_params()
					param["identifier"] = task_id;

					NewTask.params = json.dumps(param);

					NewTask.save();
					print(NewTask.experiment)
					return_tasks.append(NewTask);

				#return HttpResponse('{"params":' + str(params) + "}")
			for workertask in find_tasks:
				return_tasks.append(workertask);

			params_list = []

			response = "";

			for task in return_tasks:
				params = task.params
				params_json = byteify(json.loads(params));
				if (task.results == "null"):
					params_list.append(params_json);
					print(params_json);

			return HttpResponse('{"params":' + str(params_list) + "}")

			#return HttpResponse(return HttpResponse('{"params":' + str(params) + "}"), content_type='application/json; charset=utf-8')

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")