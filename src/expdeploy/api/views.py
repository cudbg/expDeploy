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
import boto3
import boto.mturk.connection
from boto.mturk.connection import MTurkRequestError
from boto.mturk.qualification import Qualifications, \
        PercentAssignmentsApprovedRequirement,\
        PercentAssignmentsSubmittedRequirement,\
        LocaleRequirement, NumberHitsApprovedRequirement
        #get function from qualifications
import datetime
import traceback
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

import logging

# Get an instance of a logger
logger = logging.getLogger('api')

import heapq


###############################
#
# The MTurk APIs are not great.  The following will be useful
#
# Boto3 mturk python library
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html
#
# Example code:
# https://github.com/aws-samples/mturk-code-samples/blob/master/Python/CreateHitSample.py
#
# MTurk API reference:
# https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_DataStructuresArticle.html
#
####################################3

SANDBOXHOST = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# 'mechanicalturk.sandbox.amazonaws.com'
REALHOST = 'https://mturk-requester.us-east-1.amazonaws.com'
# 'mechanicalturk.amazonaws.com'

def get_mturk_connection(access_key, secret, is_sandbox):
  host = SANDBOXHOST
  if (is_sandbox in ("False", False)):
    host = REALHOST
  logger.info("is_sandbox: %s" % is_sandbox)
  logger.info("AWS info: accesskey: %s" % access_key)
  logger.info("AWS secret: %s" % secret)
  logger.info("AWS host: %s" % host)

  try:
    mturk = boto3.client('mturk',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret,
        region_name = 'us-east-1',
        endpoint_url = host
    )
  except Exception as e:
      logger.error("Failed to get mturk connection")
      logger.error(traceback.format_exc())
      raise e

  try:
    logger.info("mturk balance: %s" %  str(mturk.get_account_balance())[:50])
  except Exception as e:
      logger.error("Failed to get account balance")
      logger.error(traceback.format_exc())
      raise e

  return mturk



def changeKey(dictionary, oldKey, newKey):
  dictionary[newKey] = dictionary[oldKey]
  del dictionary[oldKey]
  return dictionary



def showResults(request):
  """
  Example of how to create a custom page to view the results of an experiment
  """

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
    logger.info("showResults2: " + task.wid)
    js = json.loads(task.results)
    data = js["data"]
    if len(data) > 0:
      lastResult = data[len(data)-1]

      # check answer attribute
      if "summaryModel" in lastResult:
        resp = lastResult["summaryModel"]
        logger.info(lastResult["summaryModel"])

      logger.info(lastResult.get("summary", ""))

  return resp

if __name__ =="__main__":
  # using this, you can run views in the console manually
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
  logger.info("")
  logger.info("logAnalytics/")
  usrId = request.POST.get("usrId", '');
  expId = request.POST.get('expId', '');
  logger.info(usrId)
  logger.info(expId)
  logger.info(request.POST["data"])

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
  mturk = get_mturk_connection(key, secret_key, False)

  approve = mturk.approve_assignment(
          AssignmentId="39JEC7537VK9RX8SMLEVMEW0WN3VCN",
          OVerrideRejection=True)
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
      mturk = get_mturk_connection(key, secret_key, paySandbox)

      balance = float(mturk.get_account_balance()['AvailableBalance'])

      BONUS = exp.bonus_payment
      PERTASK = exp.per_task_payment

      p = PERTASK * float(completed)
      if completions[assignmentId]:
        p = BONUS + PERTASK * float(completed)
        if PERTASK * float(completed) + BONUS > balance:
          return HttpResponse("Insufficient funds. Please refill your account on Amazon.")


      if PERTASK * float(completed) > balance:
        return HttpResponse("Insufficient funds. Please refill your account on Amazon.")

      try:
        approve = mturk.approve_assignment(AssignmentId=assignmentId)
      except MTurkRequestError as e:
        print(e)

      bon = mturk.send_bonus(
              WorkerId=wid,
              AssignmentId=assignmentId,
              BonusAmount=str(p),
              Reason="GREAT WORK! bonus + per task payments"
      )
      logger.info("sent bonus")
      logger.info(bon)


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
  #       sss = task.historyevent_set.all()
  #       for his in sss:
  #               histories.append(his)
  #       metadata.append(task.metaData)
  #       print("SSS" + task.experiment.name)
  #       d = byteify(json.loads(task.results));
  #       data.append(d);

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
  """
  Delete a HIT from mturk.  
  First need to set its expiration to "now" and then delete it
  """
  isSandbox = request.GET.get('isSandbox', '');
  expId = request.GET.get('experiment', '');
  usrId = request.GET.get('researcher', '');
  researcher = Researcher.objects.filter(user__username=usrId)[0];
  exp = ExperimentModel.objects.filter(name=expId,username=usrId)[0];

  key = researcher.aws_key_id;
  secret_key = researcher.aws_secret_key;
  mturk = get_mturk_connection(key, secret_key, isSandbox)

  # Get HIT status
  status = mturk.get_hit(HITId=exp.hitID)['HIT']['HITStatus']
  logger.info('HITStatus: %s for %s' % (status, exp.hitID))

  # If HIT is active then set it to expire immediately
  if status in ('Assignable', 'Unassignable'):
    logger.info("Setting expiration to 2015 for %s" % exp.hitID)
    response = mturk.update_expiration_for_hit(
      HITId=exp.hitID,
      ExpireAt=datetime.datetime(2015, 1, 1)
    )        
    logger.info(response)

  try:
    logger.info("expired the HIT.  Now deleting")
    disable = mturk.delete_hit(HITId=exp.hitID)
    logger.info(disable)
  except Exception as e:
    logger.error(traceback.format_exc())
    messages.add_message(request,
        messages.ERROR, 'Failed to delete HIT: %s' % str(e))
    raise e

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

  logger.info("")
  logger.info("called /mturk")
  logger.info(request.GET)

  key = researcher.aws_key_id;
  secret_key = researcher.aws_secret_key;
  mturk = get_mturk_connection(key, secret_key, isSandbox)

  url = request.GET.get('URL', '');
  title = expId.replace("_"," ")
  hit_title = exp.hit_title.replace("_"," ")
  description = exp.hit_description

  keys = exp.hit_keywords.split(',');
  keywords = ", ".join([k.strip() for k in keys])

  # the height of the iframe holding the external hit
  frame_height = exp.hit_frame_height
  amount = exp.hit_submission_payment

  questionform = boto.mturk.question.ExternalQuestion( url, frame_height )

  #
  # create qualifications for the experiment
  #
  experiment_quals = exp.qualificationsmodel_set
  account_name = exp.username
  q_set = experiment_quals.get(username=account_name)

  quals = []
  if q_set.US_only:
    quals.append(dict(
      QualificationTypeId="00000000000000000071",
      Comparator="EqualTo",
      LocaleValues=[dict(Country="US")]
    ))

  if isSandbox == "False":
    # Num Hits Approved
    quals.append(dict(
      QualificationTypeId= "00000000000000000040",
      Comparator= "GreaterThanOrEqualTo",
      IntegerValues= [1]
    ))

  # quals.append({
  #     QualificationTypeId: "000000000000000000L0",
  #     Comparator: "GreaterThanOrEqualTo",
  #     IntegerValues: [q_set.percentage_hits_approved]
  # })

  # q_set.percentage_hits_approved
  # q_set.percentage_assignments_submitted

  expiration = datetime.datetime.now() + datetime.timedelta(seconds=exp.hit_duration_in_seconds)

  logger.info("calling mturk.create_hit")
  create_hit_result = mturk.create_hit(
      Title = hit_title,
      Description = description,
      Keywords = keywords,
      Question = questionform.get_as_xml(),
      Reward = str(amount),
      MaxAssignments=exp.n,
      AssignmentDurationInSeconds=exp.hit_duration_in_seconds,
      LifetimeInSeconds=exp.hit_duration_in_seconds,
      QualificationRequirements = quals
      #response_groups = ( 'Minimal', 'HITDetail' ) # I don't know what response groups are
  )

  hit_type_id = create_hit_result['HIT']['HITTypeId']
  hit_id = create_hit_result['HIT']['HITId']
  exp.hitID = hit_id
  logger.info(create_hit_result)
  logger.info("done.  Got hitid %s" % exp.hitID)

  if isSandbox == "True":
    exp.published_sandbox = True
    messages.add_message(request,
            messages.SUCCESS, 'Experiment successfully posted to Sandbox.')
  else:
    exp.published_mturk = True
    messages.add_message(request,
            messages.SUCCESS, 'Experiment successfully posted to MTurk.')
  exp.save()

  return HttpResponseRedirect(reverse(ProfileGalleryView));

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
    try:
      logger.info("log with wid " + request.POST.get("worker_id", ''))


      body_unicode = request.body.decode('utf-8')
      body = json.loads(body_unicode)
      #body = request.POST.dict()

      #TODO: Filter by experiment name

      find_tasks = WorkerTask.objects.filter( wid=body["worker_id"],name=body["task_name"],identifier=body["task_id"]);
      logger.info("found %d tasks" % len(find_tasks));


      logger.info("wid:      %s" % body["worker_id"])
      logger.info("taskname: %s" % body["task_name"])
      logger.info("taskid:   %s" % body["task_id"])

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
    except Exception as e:
      logger.error(str(e))
      logger.error(traceback.format_exc())
      raise e
    return HttpResponse("success");


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
  n = int(request.GET.get('n', '1'));

  logger.info("get %d tasks for wid %s" % (n, wid))

  exps = ExperimentFile.objects.filter(username=usrId,experiment__name=expId);
  if len(exps)==0:
    return HttpResponse("No experiments with those specs found")

  expsBackwards = reversed(exps);

  expModel = ExperimentModel.objects.filter(name=expId,username=usrId)[0];
  wids = json.loads(expModel.banned)["ids"]


  for exp in expsBackwards:

    logger.info(exp.original_filename)
    if (exp.original_filename == (expModel.config_file)):
      EX = exp.experiment

      if wid in wids:
        return HttpResponse("Your WorkerID has been banned")

      his = json.loads(EX.analytics)
      if "wids" not in his:
        his["wids"] = []

      return_tasks = []
      find_tasks = WorkerTask.objects.filter(name=taskName, wid=wid, experiment=EX);

      logger.info("found %d tasks in database" % len(find_tasks))
      logger.info(str(find_tasks))

      if (len(find_tasks) == 0):
        data = json.loads(exp.docfile.read())
        logger.info(data["tasks"])

        for task in data["tasks"]:
          logger.info("params for task name %s.  Checking if it is same as '%s'" % (task['name'], taskName))
          if task["name"] == taskName:

            param = {}
            gen = [{}]

            # Create all combinatinos of the parameters' values
            for p in task["params"]:
              if p["type"] == "UniformChoice":
                gen2 = []
                for inProgress in gen:
                  for choice in p["options"]:
                    modify = copy(inProgress)
                    modify[p["name"]] = choice
                    gen2.append(modify)
                gen = gen2

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



            logger.info("generating %d tasks" % n)
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

              task_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
              NewTask = WorkerTask(
                  name=taskName, 
                  wid=wid, 
                  experiment=EX, 
                  identifier=task_id, 
                  researcher=usrId,
                  hitId=mturk_hitId,
                  assignmentId=mturk_assignmentId
              )



              param["identifier"] = task_id;
              NewTask.params = json.dumps(param);

              history = json.loads(NewTask.history)
              timestamp_string = format(datetime.datetime.now(), u'U')
              event = {"type":"changeStatus","newStatus":"Waiting","timestamp":timestamp_string}
              history["events"].append(event)
              NewTask.history = json.dumps(history)

              NewTask.isSandbox = isSandbox
              NewTask.save();
              return_tasks.append(NewTask);


            logger.info("created %d tasks" % len(return_tasks))
            EX.analytics = json.dumps(his)
            EX.balanced_history=json.dumps(balanced_history)
            EX.save()

      for workertask in find_tasks:
        return_tasks.append(workertask);

      params_list = []
      for task in return_tasks:
        params = json.loads(task.params)
        #params_json = byteify(params);

        results = json.loads(task.results)
        if (len(results["data"]) == 0 and task.currentStatus=="Waiting"):
          params_list.append(params);

      response = dict(
        params=params_list,
        pay=EX.per_task_payment,
        bonus=EX.bonus_payment
      )
      return HttpResponse(json.dumps(response))

      return HttpResponse('{"params":' + str(params_list) + ',"pay":' + str(EX.per_task_payment) + ',"bonus":' + str(EX.bonus_payment) + '}')


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
