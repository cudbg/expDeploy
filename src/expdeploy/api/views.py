from __future__ import division
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import simplejson as json
#from .models import Experiment
from .models import WorkerTask

from random import randint
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
from boto.mturk.connection import MTurkRequestError
from boto.mturk.qualification import Qualifications, \
	PercentAssignmentsApprovedRequirement,\
	PercentAssignmentsSubmittedRequirement,\
	LocaleRequirement, NumberHitsApprovedRequirement
	#get function from qualifications 
import datetime
import csv
from django.utils.encoding import smart_str
from StringIO import StringIO
from random import shuffle
from random import seed
import cStringIO as StringIO

from django.db import connection
from os import system
import os, tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
#from sendfile import sendfile
import os
import pwd

import heapq

def changeKey(dictionary, oldKey, newKey):
	dictionary[newKey] = dictionary[oldKey]
	del dictionary[oldKey]
	return dictionary




def showResults(request):

	save = request.GET.get('save', '');

	wids = ["A37S96RT1P1IT2", "A18TCR555RWUZV", "A1945USNZHTROX", "A2JCHN90PRUWDH","A27PVIL93ZMY46","A1CA46R2A6TV9W","ANMXMEB55AGM6","A2DVZVTZOCUUB","A1909MOQZUXZZ5","A24NUJ0TMY0GBG","A377LTGWJKY2IW","A3VEGU07DAYV4T","A9JLQEN9J5WL3","A1MYLQQL8BBOYT","A1EQ2HDHF2WWSY","A1KWJ1MMFJB515","A1640H4RXH8NZE","A25N0K40JAZTN1","A1T2NVE4DGCDFL","AOTF48KUV9KWM","A2IA303OT5BBX0","A2K7AVZWEC9B14","A1RILUP7EBYOQ1","A40LU73SS18IW",
	"A13HO1CD5GOQTQ","A3O2NOP1NUWCWL","A1PBRKFHSF1OF8","A39W3PYK82IBAS","A5EU1AQJNC7F2","A3JX5WINGY8PEM","APSDY7ALAEWUD","ATMQRDBW7WM1Z","ATMQRDBW7WM1Z","AIYYLYN9AM5FQ","AN5W1383SSGO4", "ABMX8XUNPR3LP","ABMX8XUNPR3LP","A3D5TVDZE407DE","A3KN0O7VP8YSZY", "ALWCL6V9K2D00","A11YS0T8MV3Q7C","A2G6V5N4WQLPEN","A16FVD94WDZNAS"]

	confidence_spam = ["A3O2NOP1NUWCWL", "A39W3PYK82IBAS", "A2JCHN90PRUWDH", "A2DVZVTZOCUUB", "A24NUJ0TMY0GBG"]
	explanation_spam = ["A13HO1CD5GOQTQ", "A1640H4RXH8NZE", "A1909MOQZUXZZ5", "A24NUJ0TMY0GBG", "A25N0K40JAZTN1", "A2DVZVTZOCUUB", "A39W3PYK82IBAS", "A3VEGU07DAYV4T", "AN5W1383SSGO4"]

	spam = explanation_spam + confidence_spam

	for sp in spam:
		if sp in wids:
			wids.remove(sp)

	paramList = {}
	for i in range(0,500):
		paramList[str(i)] = 0

	find_tasks = WorkerTask.objects.filter(experiment__name='Label_Product_Review_Snippets')

	dataZ = []

	remaining = []

	for task in find_tasks:
		if task.wid not in wids:
			continue
		js = json.loads(task.results)
		data = js["data"]
		if len(data) > 0:
			lastResult = data[len(data)-1]
			lastResult["WID"] = task.wid
			lastResult = changeKey(lastResult, "labeledHelpful", "humanVoteHelpful")
			lastResult = changeKey(lastResult, "summaryModel", "modelHumanAgree")
			if lastResult["modelHumanAgree"] == "LabeledMachineCorrectly":
				lastResult["modelHumanAgree"] = True
			else:
				lastResult["modelHumanAgree"] = False
			lastResult = changeKey(lastResult, "summary", "reviewHumanAgree")
			if lastResult["reviewHumanAgree"] == "LabeledCorrectly":
				lastResult["reviewHumanAgree"] = True
			else:
				lastResult["reviewHumanAgree"] = False

			if lastResult["reviewHumanAgree"]:
				lastResult["reviewVoteHelpful"] = lastResult["humanVoteHelpful"]
			else:
				lastResult["reviewVoteHelpful"] = not lastResult["humanVoteHelpful"]

			if lastResult["modelHumanAgree"]:
				lastResult["modelVoteHelpful"] = lastResult["humanVoteHelpful"]
			else:
				lastResult["modelVoteHelpful"] =  not lastResult["humanVoteHelpful"]

			lastResult["modelReviewAgree"] = lastResult["modelVoteHelpful"] == lastResult["reviewVoteHelpful"]
		#	if lastResult[""]
			#del dictionary[old_key]
			dataZ.append(lastResult)
			if "summaryModel" in lastResult:
				paramList[str(lastResult["segmentID"])]+=1
	output = ""
	for i in range(0,500):
		output = output + "\n" + str(paramList[str(i)]) + "\n" + str(i)

	for i in range(0,500):
		if paramList[str(i)] == 2:
			remaining.append(i)
		if paramList[str(i)] == 1:
			remaining.append(i)
			remaining.append(i)
		if paramList[str(i)] == 0:
			remaining.append(i)
			remaining.append(i)
			remaining.append(i)


	shuffle(remaining)


	ignores = []

	for i in range(0,500):

		if paramList[str(i)] == 3 or paramList[str(i)] == 4 or paramList[str(i)] == 2 or paramList[str(i)] == 5:
			votes1 = []
			votes2 = []
			votes3 = []
			for dat in dataZ:
				if dat["segmentID"] == i:
					if "summaryModel" in dat:
						votes1.append(dat["summaryModel"])
						votes2.append(dat["labeledHelpful"])
						votes3.append(dat["summary"])
			if len(votes1) == 2:
				if votes1[1] == votes1[0]:
					votes1.append(votes1[0])
					votes2.append(votes2[0])
					votes3.append(votes3[0])
				else:
					output = output + "haaa" + str(i) + "haaaaaa"

			if len(votes1) == 4:
 				votes1 = [votes1[1],votes1[2],votes1[3]]
 				votes2 = [votes2[1],votes2[2],votes2[3]]
			if len(votes1) == 3 or len(votes1) == 5:
				vote = max(set(votes1), key=votes1.count)
				vote2 = max(set(votes2), key=votes2.count)
				vote3 = max(set(votes3), key=votes3.count)
				output = output + "\n" + str(vote) + str(i) + str(vote2) + str(vote3) + "hi"

				print >>sys.stderr, "\n" + str(votes1)

	print >>sys.stderr, remaining

					
	print >>sys.stderr, len(remaining)

	expModel = ExperimentModel.objects.filter(name="Label_Product_Review_Snippets")[0];
	hist = json.loads(expModel.balanced_history)
	hist["pickFrom"] = remaining
	expModel.balanced_history = json.dumps(hist)
	if save != '':
		expModel.save()

	# myfile = StringIO.StringIO()
	# for line in dataZ:
	# 	myfile.write(json.dumps(line) + "\n")
	# response = HttpResponse(FileWrapper(myfile.getvalue()), content_type='application/zip')
	# response['Content-Disposition'] = 'attachment; filename=myfile.zip'


	myfile = StringIO.StringIO()
	for line in dataZ:
		myfile.write(json.dumps(line) + "\n")

	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=authors_list.txt'
	response.write(myfile.getvalue())
	return response


	return response


	return HttpResponse(output)


def showResults2(request):


	wids = ["A26Y58YECZUZZG", "A37S96RT1P1IT2", "A18TCR555RWUZV", "A1945USNZHTROX", "A2JCHN90PRUWDH"]
	expId = request.GET.get('wid', '');
	if expId != '':
		wids = [expId]

	tasks = []
	for wid in wids:
		find_tasks = WorkerTask.objects.filter(wid=wid)
		for task in find_tasks:
			tasks.append(task)

	resp = ""

	for task in tasks:
		#print(task.results)
		print(task.wid)
		js = json.loads(task.results)
		data = js["data"]
		if len(data) > 0:
			lastResult = data[len(data)-1]
			if "summaryModel" in lastResult:
				resp = lastResult["summaryModel"]
				print(lastResult["summaryModel"])

			print(lastResult["summary"])

	return resp


def showResults3(request):
	wids = ['A3G00Q5JV2BE5G','A190R7H2ZY8KWY','ATEL480BFZ1F6','A1X0H6VAK3AQE9','A3N8JP3QR3VPE8','A2WYJOE2OUCAQ2','A33FA1VLSTBM74','AGRKG3YT3KMD8','A1MYLQQL8BBOYT','A365SN61J4UNGR','A1KBL89VYQR0FT','A1MADOUB1BA0A5','A11YS0T8MV3Q7C','A3BZO7NGC7REGI']
	tasks = []
	for wid in wids:
		find_tasks = WorkerTask.objects.filter(wid=wid)
		for task in find_tasks:
			tasks.append(task)	

	respText = ""
	for task in tasks:
		#print(task.results)
		print(task.wid)
		js = json.loads(task.results)
		data = js["data"]
		if len(data) > 0:
			print(data)

		tryThis = json.loads(data)
		respText += str(tryThis[0]) + "\n"

		respText += str(task.wid) + "\n"
		respText += str(data) +"\n"
		respText += "\n\n\n"

	response = HttpResponse(respText, content_type="text/plain")
	return response



if __name__ =="__main__":
	showResults3("hello world")

def hasStarted(request):
	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	taskName = request.GET.get('task', '');
	wid = request.GET.get('wid', '');

	print(wid)
	print(expId)
	print(usrId)

	expModel = ExperimentModel.objects.filter(name=expId,username=usrId)[0];

	find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment__name=expId);
	
	taskCount = 0
	for task in find_tasks:
		if (task.experiment == expModel):
			taskCount+=1

	if (taskCount > 0):
		for task in find_tasks:
			if task.currentStatus=="Waiting":
				return HttpResponse('true')
			
		return HttpResponse('done')
	else:
		return HttpResponse('false')



def logAnalytics(request):
	print(request.POST["data"])
	usrId = request.POST.get("usrId", '');
	expId = request.POST.get('expId', '');	
	print(request.POST)
	print(usrId)
	print(expId)

	exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];
	js = json.loads(exp.analytics)
	js["log"].append(request.POST["data"])
	exp.analytics = json.dumps(js)
	exp.save()
	return HttpResponse(request.POST)

def approve(request):
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
				if PERTASK * float(completed) + BONUS > balance:
					return HttpResponse("Insufficient funds. Please refill your account on Amazon.")


			if PERTASK * float(completed) > balance:
				return HttpResponse("Insufficient funds. Please refill your account on Amazon.")

			try: 
				approve = mturk.approve_assignment(assignmentId)
			except MTurkRequestError as e:
				print(e)
			
			bon = mturk.grant_bonus(wid, assignmentId, p, "GREAT WORK! bonus + per task payments")


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

def exportCSV(request):

	expId = request.GET.get('experiment', '');
	usrId = request.GET.get('researcher', '');
	print(usrId)
	#TODO: Filter by experiment name
	find_tasks = WorkerTask.objects.filter(experiment__name=expId, researcher=usrId);
	data = []
	for task in find_tasks:
		print("SSS" + task.experiment.name)
		d = byteify(json.loads(task.results));
		data.append(d);

	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response, csv.excel)
	response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

	response['Content-Disposition'] = 'attachment; filename=export.csv'
	writer = csv.writer(response, csv.excel)
	writer.writerow([
		smart_str(u"ID"),
		smart_str(u"Name"),
		smart_str(u"Parameters"),
		smart_str(u"Results"),
		smart_str(u"History"),
		smart_str(u"Status"),
		smart_str(u"Paid"),
		smart_str(u"WID"),
		])
	for obj in find_tasks:
		writer.writerow([
			smart_str(obj.pk),
			smart_str(obj.name),
			smart_str(obj.params),
			smart_str(obj.results),
			smart_str(obj.history),
			smart_str(obj.currentStatus),
			smart_str(obj.paid),
			smart_str(obj.wid),
			])
	return response

	print(data);
	return HttpResponse(data)

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


	system("pg_dump -d gpaasdb -f " + '/home/ubuntu/expDeploy/'+str(usrId)+'.dump ' + "-t api_metadata_temp -t api_workertask_temp")
	filename = "/home/ubuntu/expDeploy/" + str(usrId) +".dump" # Select your file here.                                
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
	title = expId.replace("_"," ")
	hit_title = exp.hit_title.replace("_"," ")
	description = exp.hit_description


	keys = exp.hit_keywords.split(',');
	


	keywords = []
	for k in keys:
		keywords.append(k.strip());
	frame_height = exp.hit_frame_height# the height of the iframe holding the external hit
	amount = exp.hit_submission_payment
	 
	questionform = boto.mturk.question.ExternalQuestion( url, frame_height )

	#get set of qualifications for specific experiment
	experiment_quals = exp.qualificationsmodel_set
	account_name = exp.username
	q_set = experiment_quals.get(username=account_name)
	
	approved_req = PercentAssignmentsApprovedRequirement(comparator = "GreaterThan",
		integer_value = q_set.percentage_hits_approved)
	submitted_req = PercentAssignmentsSubmittedRequirement(comparator = "GreaterThan",
		integer_value = q_set.percentage_assignments_submitted)
	if q_set.US_only:
		locale_req = LocaleRequirement("EqualTo", "US")
	#Hardcoded qualification for now. Will change later.
	#number_approved_req = NumberHitsApprovedRequirement(comparator = "GreaterThan", integer_value = "500")
	qualifications = Qualifications()
	#qualifications.add(approved_req)
	#qualifications.add(submitted_req)
	#qualifications.add(locale_req)
	#qualifications.add(number_approved_req)

	hit_duration = datetime.timedelta(seconds=exp.hit_duration_in_seconds)	

	if (isSandbox == "False"):
		number_approved_req = NumberHitsApprovedRequirement(comparator = "GreaterThan", integer_value = "50")
		qualifications.add(approved_req)
		qualifications.add(submitted_req)
		qualifications.add(locale_req)
		qualifications.add(number_approved_req)
	 
	create_hit_result = mturk.create_hit(
	    title = hit_title,
	    description = description,
	    keywords = keywords,
	    question = questionform,
	    reward = boto.mturk.price.Price( amount = amount),
	    max_assignments=exp.n,
	    duration=hit_duration,
	    qualifications = qualifications,
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

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

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

		

		#print(request.POST)
		#print(request.body)
		print(request.POST.get("worker_id", ''))

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



		m = Metadata(userAgent=metaData["userAgent"], dimensions=metaData["dimension"], start=metaData["taskStart"], end=metaData["taskFinish"],ip_address=get_client_ip(request),wid=body["worker_id"])

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

	exps = ExperimentFile.objects.filter(username=usrId,experiment__name=expId);
	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")


	
	return_tasks = []
	find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment__name=expId);
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

			timestamp_string = format(datetime.datetime.now(), u'U')
			event = HistoryEvent(newStatus="Stopped", timeStamp=int(timestamp_string))
			event.workerTask = task
			event.save()


			task.save()
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

	exps = ExperimentFile.objects.filter(username=usrId,experiment__name=expId);
	if len(exps)==0:
		return HttpResponse("No experiments with those specs found")

	expsBackwards = reversed(exps);

	expModel = ExperimentModel.objects.filter(name=expId,username=usrId)[0];
	wids = json.loads(expModel.banned)["ids"]


	for exp in expsBackwards:

		print(exp.original_filename)
		if (exp.original_filename == (expModel.config_file)):
			print("test 2");

			EX = exp.experiment
			print("n2222"+EX.name);
			


			if wid in wids:
				return HttpResponse("Your WorkerID has been banned")

			his = json.loads(EX.analytics)
			if "wids" not in his:
				his["wids"] = []


			return_tasks = []
			find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment=EX);
			print(find_tasks);
			if (len(find_tasks) == 0):
				
				

				print >>sys.stderr, 'docfile below!'
				
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

						while n > len(gen):
							gen.append({})


						

						balanced_history = json.loads(EX.balanced_history)
						for p in task["params"]:
							if p["type"] == "CountDownChoice":
								if p["name"] not in balanced_history:
									balanced_history[p["name"]] = {}

									for i in range(0, len(p["options"])):
										balanced_history[p["name"]][p["options"][i][1]] = p["options"][i][0]

						balanced_history = json.loads(json.dumps(balanced_history))
						pickedsofar = {}



						for i in range(0,n):
							
							param = gen.pop()

							

							for p in task["params"]:

								if p["name"] not in pickedsofar:
									pickedsofar[p["name"]] = []
								

								if p["type"] == "CountDownChoice":

									sorter = []

									historical_data = balanced_history[p["name"]]
									possibilities = historical_data.keys()
									possible_values = []

									for key in possibilities:
										if historical_data[key] > 0:
											possible_values.append(key)

									print(possible_values)

									if len(possible_values) == 0:
										historical_data = {}
										for i in range(0, len(p["options"])):
											historical_data[p["options"][i][1]] = p["options"][i][0]
											possible_values.append(p["options"][i][1])

									shuffle(possible_values)
									picked = possible_values[0]

									historical_data[picked] -= 1
									balanced_history[p["name"]] = historical_data 


									param[p["name"]] = picked
									# pickFrom = balanced_history["pickFrom"]
									# shuffle(pickFrom)

									# picked = 0

									# if len(pickFrom) > 0:

									# 	picked = pickFrom[0]
									# 	while picked in pickedsofar[p["name"]]:
									# 		shuffle(pickFrom)
									# 		picked = pickFrom[0]
									# else:
									# 	picked = random.randint(0,500)

									# for key in historical_data:
									# 	if historical_data[key] < 3 and key not in pickedsofar[p["name"]]:
									# 		sorter.append(key)

									# shuffle(sorter)

									# if len(sorter) == 0:
									# 	balanced_history[p["name"]] = {}
									# 	for i in range(p["options"][0], p["options"][1]):
									# 		balanced_history[p["name"]][str(i)] = 0

									# 	historical_data = balanced_history[p["name"]]

									# 	for key in historical_data:
									# 		if historical_data[key] < 3 and key not in pickedsofar[p["name"]]:
									# 			sorter.append(key)

									# shuffle(sorter)

									# minHist = 999
									# for key in sorter:
									# 	minHist = min(minHist, balanced_history[p["name"]][key])

									# sorter2 = []
									# for key in sorter:
									# 	if balanced_history[p["name"]][key] <= minHist:
									# 		sorter2.append(key)

									# shuffle(sorter2)
									# sorter = sorter2

									# numchoose = sorter[0]

									# print(numchoose)
									# print(pickedsofar[p["name"]])


									

									# pickedsofar[p["name"]].append(numchoose)

									# #print(numchoose[1])
									# #print(numchoose[0])
									# balanced_history[p["name"]][numchoose]+=1

									# param[p["name"]] = picked
									# pickedsofar[p["name"]].append(picked)
									# if len(pickFrom) > 0:
									# 	pickFrom.pop(0)
									# balanced_history["pickFrom"] = pickFrom

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

							return_tasks.append(NewTask);


							#print(NewTask.experiment)


						EX.analytics = json.dumps(his)
						#for key in balanced_history:
						EX.balanced_history=json.dumps(balanced_history)
						EX.save()


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
