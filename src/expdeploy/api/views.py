from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
#from .models import Experiment
from .models import WorkerTask
from .models import HistoryEvent
from .models import Metadata
from copy import copy
from zipfile import ZIP_DEFLATED, ZipFile

import sys
from planout.ops.random import *
from expdeploy.gpaas.models import ExperimentFile
from expdeploy.gpaas.models import Researcher
from expdeploy.gpaas.models import ExperimentModel
from expdeploy.gpaas.views import ProfileGalleryView
from django.utils.dateformat import format
import importlib;
import random
import string
import boto.mturk.connection
from boto.mturk.qualification import Qualifications, \
	PercentAssignmentsApprovedRequirement,\
	PercentAssignmentsSubmittedRequirement
	#get function from qualifications 
import datetime
import csv
import json
from django.utils.encoding import smart_str
from StringIO import StringIO
from random import shuffle
from random import seed

from django.db import connection
from os import system
import os, tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
#from sendfile import sendfile
import os
import pwd

def approve():
	researcher = Researcher.objects.filter(user__username="hn2284")[0];
	key = researcher.aws_key_id;
	secret_key = researcher.aws_secret_key;
	host = 'mechanicalturk.amazonaws.com'
	
	mturk = boto.mturk.connection.MTurkConnection(
	    aws_access_key_id = key,
	    aws_secret_access_key = secret_key,
	    host = host,
	    debug = 1 # debug = 2 prints out all requests.
	)
	 
	print boto.Version 
	print mturk.get_account_balance() 

	
	approve = mturk.approve_rejected_assignment("39JEC7537VK9RX8SMLEVMEW0WN3VCN")
	return HttpResponse("done");

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def ban(request):
	usrId = request.GET.get('researcher', '');
	expId = request.GET.get('experiment', '');	
	exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];
	wids = json.loads(exp.banned)
	wids["ids"].append(request.GET.get('wid', ''))
	exp.banned = json.dumps(wids)
	exp.save()
	return (HttpResponse(str(exp.banned)))

def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()

def allPay(request):
	usrId = request.GET.get('researcher', '');
	expId = request.GET.get('exp', '');
	find_tasks = WorkerTask.objects.filter(experiment__name=expId,researcher=usrId)
	
	print >>sys.stderr, 'Goodbye, cruel world!'
	print >>sys.stderr, str(find_tasks)

	completions = {}


	

	return HttpResponse(str(find_tasks))

def payout(request):
	assignmentId = request.GET.get('assignmentId', '');
	completed = request.GET.get('completed', '');
	assigned = request.GET.get('assigned', '');
	usrId = request.GET.get('researcher', '');
	expId = request.GET.get('exp', '');
	bonus = (completed == assigned)


	assignIds = []

	completions = {}
	waitingAssignments = []

	if assignmentId == '':
		find_tasks = WorkerTask.objects.filter(experiment__name=expId,researcher=usrId)
		print >>sys.stderr, ("TASKS BELOW")
		print >>sys.stderr, (find_tasks)
		print >>sys.stderr, (expId)
		print >>sys.stderr, (usrId)




		for task in find_tasks:


			if task.currentStatus == "Waiting":
				waitingAssignments.append(task.assignmentId)

			if task.assignmentId not in completions:
				if task.currentStatus=="Complete":
					completions[task.assignmentId] = True
				else:
					completions[task.assignmentId] = False

				assignIds.append(task.assignmentId)
			if task.currentStatus != "Complete":
				completions[task.assignmentId] = False

		print(find_tasks)
	else:
		assignIds.append(assignmentId)
		completions[assignmentId] = bonus

	for assignmentId in assignIds:

		if assignmentId not in waitingAssignments:


			
			print >>sys.stderr, (assignmentId)


			shouldBreak = False



			find_tasks = WorkerTask.objects.filter(assignmentId=assignmentId);
			wid = ""
			completed = 0

			paySandbox = find_tasks[0].isSandbox

			for t in find_tasks:
				if t.paid == True:
					shouldBreak = True

				if t.currentStatus == "Complete":
					completed+=1

				wid = t.wid


			print >>sys.stderr, (shouldBreak)

			if shouldBreak:
				continue


			researcher = Researcher.objects.filter(user__username=usrId)[0];
			exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];

			key = researcher.aws_key_id;
			secret_key = researcher.aws_secret_key;
			host = 'mechanicalturk.sandbox.amazonaws.com'

			if (paySandbox == False):
				host = 'mechanicalturk.amazonaws.com'
			
			mturk = boto.mturk.connection.MTurkConnection(
			    aws_access_key_id = key,
			    aws_secret_access_key = secret_key,
			    host = host,
			    debug = 1 # debug = 2 prints out all requests.
			)
			 
			#print boto.Version 
			balance = mturk.get_account_balance() 


			assignmnet = mturk.get_assignment(assignmentId)

			#print(assignmnet.AssignmentStatus)

			BONUS = exp.bonus_payment
			PERTASK = exp.per_task_payment

			p = mturk.get_price_as_price(PERTASK * float(completed))
			if completions[assignmentId]:
				p = mturk.get_price_as_price(BONUS + PERTASK * float(completed))

			if p + BONUS > balance:
				return HttpResponse("Insufficient funds. Please refill your account on Amazon.")

			approve = mturk.approve_assignment(assignmentId)
			
			bon = mturk.grant_bonus(wid, assignmentId, p, "bonus + per task payments")


			# print >>sys.stderr, (bon)
			# print >>sys.stderr, (assignmentId)
			# print >>sys.stderr, (wid)

			for t in find_tasks:
				t.paid = True
				t.save()


	return HttpResponse("Payments done.")

def results(request):
	researcherId = request.GET.get('researcher', '');
	find_tasks = WorkerTask.objects.filter(researcher=researcherId);
	rows = []
	print(find_tasks)
	for workerTask in find_tasks:
		new = True
		for row in rows:
			if row['task'].assignmentId == workerTask.assignmentId:
				row['tasks']+=1
				if workerTask.currentStatus == "Complete":
					row['completed']+=1
				if workerTask.currentStatus == "Waiting":
					row['waiting'] = True
				new=False
			break

		if new == True:

			assignmentRow = {'tasks':1,'completed':0, 'task':workerTask, 'waiting':False}
			if workerTask.currentStatus == "Complete":
				assignmentRow['completed']+=1
			if workerTask.currentStatus == "Waiting":
				assignmentRow['waiting'] = True
			rows.append(assignmentRow)
	#{experiment id, task id, % of tasks completed, in progress or done, unpaid or paid, }
	print(rows)
	return HttpResponse(str(rows))

def export(request):
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	#print(usrId)
	#TODO: Filter by experiment name
	find_tasks = WorkerTask.objects.filter(experiment__name=expId, researcher=usrId);

	if len(find_tasks) == 0:
		return HttpResponse("No data to download unfortunately.")

	data = []
	metadata = []
	histories = []

	exp_num = find_tasks[0].experiment.id



	metaDataIds = []
	workerTaskIds = []
	for w in WorkerTask.objects.raw("SELECT * FROM api_workertask WHERE experiment_id=%s", [exp_num]):
		metaDataIds.append(w.metaData_id)
		workerTaskIds.append(w.id)
		#print('hi')

	cursor = connection.cursor()
	if db_table_exists("api_workertask_temp"):
		cursor.execute("DROP TABLE api_workertask_temp")
	if db_table_exists("api_metadata_temp"):
		cursor.execute("DROP TABLE api_metadata_temp")
	if db_table_exists("api_historyevent_temp"):
		cursor.execute("DROP TABLE api_historyevent_temp")
	print("\n\n\n",workerTaskIds)
	
	##workerTaskIds=[129,130]
	#cursor.execute("SELECT * INTO api_historyevent_temp FROM api_historyevent WHERE workerTask_id = ANY(%s)", [workerTaskIds]) #doesn't work
	cursor.execute("SELECT * INTO api_metadata_temp FROM api_metadata WHERE id = ANY(%s)", [metaDataIds]) #works
	cursor.execute("SELECT * INTO api_workertask_temp FROM api_workertask WHERE experiment_id=%s AND researcher=%s", [exp_num,usrId])

	# for task in find_tasks:
	# 	sss = task.historyevent_set.all() 
	# 	for his in sss:
	# 		histories.append(his)
	# 	metadata.append(task.metaData)
	# 	print("SSS" + task.experiment.name)
	# 	d = byteify(json.loads(task.results));
	# 	data.append(d);

	#-t api_historyevent_temp 
	#system("sudo su - postgres")

	#query failed: ERROR:  permission denied for relation api_metadata_temp
	#sudo -u postgres /// sudo: no tty present and no askpass program specified

	#resp = system('echo "$USER"')
	print >>sys.stderr, "-----"
	print >>sys.stderr, get_username()


	system("pg_dump -d gpaas -f " + '/home/GPaaS/expDeploy/'+str(usrId)+'.dump ' + "-t api_metadata_temp -t api_workertask_temp")
	filename = "/home/GPaaS/expDeploy/" + str(usrId) +".dump" # Select your file here.                                
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='mimetype=application/force-download')
	response['Content-Length'] = os.path.getsize(filename)

	os.remove(filename)
	return response

	#return sendfile(request, 'hn2284.dump')

	#return HttpResponse("hi")



def removemturk(request):
	isSandbox = request.GET.get('isSandbox', '');
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	researcher = Researcher.objects.filter(user__username=usrId)[0];
	exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];

	key = researcher.aws_key_id;
	secret_key = researcher.aws_secret_key;
	host = 'mechanicalturk.sandbox.amazonaws.com'

	if (isSandbox == "False"):
		host = 'mechanicalturk.amazonaws.com'
	
	mturk = boto.mturk.connection.MTurkConnection(
	    aws_access_key_id = key,
	    aws_secret_access_key = secret_key,
	    host = host,
	    debug = 1 # debug = 2 prints out all requests.
	)
	 
	print boto.Version 
	print mturk.get_account_balance() 

	 
	disable = mturk.disable_hit(exp.hitID)
	

	if isSandbox == "True":
		exp.published_sandbox = False
		messages.add_message(request,
			messages.SUCCESS, 'Experiment successfully removed from Sandbox.')
	else:
		exp.published_mturk = False
		messages.add_message(request,
			messages.SUCCESS, 'Experiment successfully removed from MTurk.')
	exp.save()

	

	return HttpResponseRedirect(reverse(ProfileGalleryView));
	#return HttpResponse("Successfully deleted from MTurk");


def mturk(request):
	isSandbox = request.GET.get('isSandbox', '');
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	researcher = Researcher.objects.filter(user__username=usrId)[0];
	exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];

	key = researcher.aws_key_id;
	secret_key = researcher.aws_secret_key;
	host = 'mechanicalturk.sandbox.amazonaws.com'

	if (isSandbox == "False"):
		host = 'mechanicalturk.amazonaws.com'
	
	mturk = boto.mturk.connection.MTurkConnection(
	    aws_access_key_id = key,
	    aws_secret_access_key = secret_key,
	    host = host,
	    debug = 1 # debug = 2 prints out all requests.
	)
	 
	print boto.Version 
	print mturk.get_account_balance() 


	url = request.GET.get('URL', '');
	title = expId
	description = exp.hit_description


	keys = exp.hit_keywords.split(',');
	


	keywords = []
	for k in keys:
		keywords.append(k.strip());
	frame_height = 500 # the height of the iframe holding the external hit
	amount = exp.bonus_payment
	 
	questionform = boto.mturk.question.ExternalQuestion( url, frame_height )

	#experiment_quals = exp.qualificationsmodel_set
	userperson = exp.username

	# qualifications = Qualifications()

	# q_set = qualifications.get(username=username)

	
	# approved_req = PercentAssignmentsApprovedRequirement(comparator = "GreaterThan",
	# 	integer_value = q_set.percentage_hits_approved)
	# submitted_req = PercentAssignmentsSubmittedRequirement(comparator = "GreaterThan",
	# 	integer_value = q_set.percentage_assignments_submitted)
	# qualifications.add(approved_req)
	# qualifications.add(submitted_req)
	
	 
	create_hit_result = mturk.create_hit(
	    title = title,
	    description = description,
	    keywords = keywords,
	    question = questionform,
	    reward = boto.mturk.price.Price( amount = amount),
	    max_assignments=exp.n,
	    #qualifications = qualifications,
	    response_groups = ( 'Minimal', 'HITDetail' ) # I don't know what response groups are
	)


	exp.hitID = create_hit_result[0].HITId

	if isSandbox == "True":
		exp.published_sandbox = True
		#include message for ProfileGallery
		messages.add_message(request,
			messages.SUCCESS, 'Experiment successfully posted to Sandbox.')
	else:
		exp.published_mturk = True
		messages.add_message(request,
			messages.SUCCESS, 'Experiment successfully posted to MTurk.')
	exp.save()
	print (create_hit_result)

	

	return HttpResponseRedirect(reverse(ProfileGalleryView));
	# return HttpResponse("Successfully posted to MTurk");



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
		#body = request.POST.dict()

		#TODO: Filter by experiment name

		find_tasks = WorkerTask.objects.filter( wid=body["worker_id"],name=body["task_name"],identifier=body["task_id"]);
		print(find_tasks);


		print >>sys.stderr, body["worker_id"]
		print >>sys.stderr, body["task_name"]
		print >>sys.stderr, body["task_id"]


		task = find_tasks[0]

		if (task.results == "null"):
			task.results = "{}";

		d = json.loads(task.results)

		metaData = body["metaData"]



		m = Metadata(userAgent=metaData["userAgent"], dimensions=metaData["dimension"], start=metaData["taskStart"], end=metaData["taskFinish"])

		m.save()

		task.metaData= m



		print(metaData)

		d["data"] = (body["data"]);

		task.results = json.dumps(d);

		history = json.loads(task.history)
		timestamp_string = format(datetime.datetime.now(), u'U')

		task.currentStatus = "Complete"

		event = HistoryEvent(newStatus="Complete", timeStamp=int(timestamp_string))
		event.workerTask = task
		event.save()

		task.save()



		#find_tasks = WorkerTask.objects.filter(name=body["task_name"], wid=body["worker_id"], experiment=body["experiment_name"]);

		return HttpResponse("success");

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

def finishTasks(request):
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	taskName = request.GET.get('task', '');
	wid = request.GET.get('wid', '');
	print("test 1");

	print("bleh")

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
			
				#return HttpResponse('{"params":' + str(params) + "}")
			for workertask in find_tasks:
				return_tasks.append(workertask);

			params_list = []

			print("THESE ARE THE STOPPED TASKS")
			print(return_tasks)

			response = "";

			for task in return_tasks:
				params = task.params
				params_json = byteify(json.loads(params));

				results = json.loads(task.results)
				if (len(results["data"]) == 0):
					task.currentStatus = "Stopped"
					params_list.append(params_json);

					history = json.loads(task.history)
					timestamp_string = format(datetime.datetime.now(), u'U')


					event = {"type":"changeStatus","newStatus":"Stopped","timestamp":timestamp_string}
					history["events"].append(event)
					
					task.history = json.dumps(history)
					task.save()
					print('heh"')
					print(params_json);

			return HttpResponse('{"params":' + str(params_list) + "}")

def task(request):
	mturk_hitId = request.GET.get('hitId', '');
	mturk_assignmentId = request.GET.get('assignmentId', '');
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	taskName = request.GET.get('task', '');
	wid = request.GET.get('wid', '');
	isSandbox = request.GET.get('sandbox', '');

	
	


	print(wid)
	n = int(request.GET.get('n', '1'));
	print("test 1");

	exps = ExperimentFile.objects.filter(username=usrId);
	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")

	expsBackwards = reversed(exps);

	expModel = ExperimentModel.objects.filter(name=expId,username=usrId)[0];
	wids = json.loads(expModel.banned)["ids"]

	if wid in wids:
		return HttpResponse("Your WorkerID has been banned")


	for exp in expsBackwards:

		print(exp.original_filename)
		if (exp.original_filename == (expModel.config_file)):
			print("test 2");

			EX = exp.experiment
			print("n2222"+EX.name);
			
			return_tasks = []
			find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment=EX);
			print(find_tasks);
			if (len(find_tasks) == 0):
				
				data = json.loads(exp.docfile.read())
				print(data["tasks"])

				for task in data["tasks"]:
					if task["name"] == taskName:

						param = {}
						gen = [{}]

						for p in task["params"]:
							if p["type"] == "UniformChoice":
								gen2 = []
								for inProgress in gen:
									for choice in p["options"]:
										modify = copy(inProgress)
										modify[p["name"]] = choice
										gen2.append(modify)
								gen = gen2
								#param[p["name"]] = random.choice(p["options"])

						param = gen[0]
						seed(abs(hash(wid)) % (10 ** 8))
						shuffle(gen)

						for i in range(0,n):
							
							param = gen.pop()

							task_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
							
							NewTask = WorkerTask(name=taskName, wid=wid, experiment=EX, identifier=task_id, researcher=usrId,hitId=mturk_hitId,assignmentId=mturk_assignmentId)
							param["identifier"] = task_id;
							NewTask.params = json.dumps(param);

							history = json.loads(NewTask.history)
							timestamp_string = format(datetime.datetime.now(), u'U')
							event = {"type":"changeStatus","newStatus":"Waiting","timestamp":timestamp_string}
							history["events"].append(event)
							NewTask.history = json.dumps(history)
							#print(NewTask.history)
							NewTask.isSandbox = isSandbox
							NewTask.save();

							#print(NewTask.experiment)
							return_tasks.append(NewTask);


			#return HttpResponse('{"params":' + str(params) + "}")
			for workertask in find_tasks:
				return_tasks.append(workertask);

			params_list = []

			response = "";

			for task in return_tasks:
				params = task.params
				params_json = byteify(json.loads(params));

				results = json.loads(task.results)
				if (len(results["data"]) == 0 and task.currentStatus=="Waiting"):
					params_list.append(params_json);
					print(params_json);

			return HttpResponse('{"params":' + str(params_list) + ',"pay":' + str(EX.per_task_payment) + ',"bonus":' + str(EX.bonus_payment) + '}')







	# for exp in expsBackwards:
	# 	if (exp.original_filename == (expId + ".py")):
	# 		print("test 2");

	# 		EX = exp.experiment
	# 		print("n2222"+EX.name);
			
	# 		return_tasks = []
	# 		find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment=EX);
	# 		print(find_tasks);
	# 		if (len(find_tasks) == 0):
	# 			Task = getattr(importlib.import_module("expdeploy." + str(exp.docfile).strip().replace(".py","").replace("/",".")), taskName)
			
	# 			print("Creating new tasks right now");
				
	# 			for i in range(0,n):
	# 				exp = Task(userid=wid+str(i));

	# 				task_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

	# 				NewTask = WorkerTask(name=taskName, wid=wid, experiment=EX, identifier=task_id, researcher=usrId)
	# 				param = exp.get_params()
	# 				param["identifier"] = task_id;

	# 				print(param)
	# 				NewTask.params = json.dumps(param);


	# 				history = json.loads(NewTask.history)
	# 				timestamp_string = format(datetime.datetime.now(), u'U')


	# 				event = {"type":"changeStatus","newStatus":"Waiting","timestamp":timestamp_string}
	# 				history["events"].append(event)
					
	# 				NewTask.history = json.dumps(history)

	# 				#print(NewTask.history)
	# 				NewTask.save();
	# 				#print(NewTask.experiment)
	# 				return_tasks.append(NewTask);

	# 			#return HttpResponse('{"params":' + str(params) + "}")
	# 		for workertask in find_tasks:
	# 			return_tasks.append(workertask);

	# 		params_list = []

	# 		response = "";

	# 		for task in return_tasks:
	# 			params = task.params
	# 			params_json = byteify(json.loads(params));

	# 			results = json.loads(task.results)
	# 			if (len(results["data"]) == 0 and task.currentStatus=="Waiting"):
	# 				params_list.append(params_json);
	# 				print(params_json);

	# 		return HttpResponse('{"params":' + str(params_list) + "}")

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
