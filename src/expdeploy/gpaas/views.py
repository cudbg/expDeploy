# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import ExperimentFile, ExperimentModel, QualificationsModel
from django.contrib.auth.models import User
from .models import Researcher
from expdeploy.api.models import WorkerTask

from .forms import LoginForm, UploadForm, UserForm, ExperimentForm,\
        QualificationsForm
from .forms import HitDescriptionForm, HitPaymentForm, \
        HitKeywordsForm, TaskNumberForm, BonusPaymentForm, \
        ConfigFileForm, TaskSubmissionPaymentForm, HitDurationForm, \
        HitTitleForm, HitFrameHeightForm, LinkForm

import os
import json
import sys


import logging

# Get an instance of a logger
logger = logging.getLogger('gpaas')



from expdeploy.api.models import WorkerTask

profile_view = 'expdeploy.gpaas.views.ProfileGalleryView'

login_view = 'expdeploy.gpaas.views.LoginView'


def ViewResults(request):
  #user
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

    if new == True:
      print("----dkasjdklsadjasjkdhsakjd-----")
      assignmentRow = {'tasks':1,'completed':0, 'task':workerTask,
              'waiting':False}
      if workerTask.currentStatus == "Complete":
        assignmentRow['completed']+=1
      if workerTask.currentStatus == "Waiting":
        assignmentRow['waiting'] = True
      rows.append(assignmentRow)
  print(rows)
  return render_to_response('viewresults.html',
          {'rows':rows,'researcher':researcherId},
          context_instance = RequestContext(request)
          )


def API(request):
  return HttpResponse("API")


def AuthenticateUser(request):
  #user
  if request.user.is_authenticated:
    return str(request.user)
  else:
    user = None
  #Send to login page if not logged in.
  if request.user.id is None:
    return render_to_response('login.html',
            {'loginform': LoginForm(), 'user': None, 'current_user': False,
            'mismatch': False, 'profileerror': True,},
            )


def AuthenticateExperiment(user, experiment):
  tmp = ExperimentModel.objects.filter(username=user).filter(name=experiment)
  if not tmp:
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return ExperimentModel.objects.filter(username=user,name=experiment)[0]


def GetExperiment(username, experiment):
  exp = ExperimentModel.objects.filter(username=username)
  #new code to prevent error
  if not exp.filter(name=experiment):
    return None
  else:
    return exp.get(name=experiment)
  #return exp.get(name=experiment)


def CreateExperimentView(request):
  #user
  if request.user.is_authenticated:
    user = str(request.user)
  else:
    user = None
  if request.user.id is None:
    return HttpResponseRedirect(reverse(login_view))

  #Upload files for post request
  if request.method == 'POST':
    form = ExperimentForm(request.POST, request.FILES)
    #Create ExperimentFile instance for each uploaded file.
    if form.is_valid():
    #get experiment
      experiment = form.cleaned_data['experiment']
      desc = form.cleaned_data['hit_description']
      payment = form.cleaned_data['per_task_payment']
      number_assignments = form.cleaned_data['number_of_assignments']
      bonus = form.cleaned_data['bonus_payment']
      hit_submission_payment = form.cleaned_data['task_submission_payment']
      hit_duration_in_seconds = form.cleaned_data['hit_duration_in_seconds']
      title = form.cleaned_data['hit_title']
      key = form.cleaned_data['hit_keywords']

      #check if experiment already exists
      temp = ExperimentModel.objects.filter(username=user)
      temp = temp.filter(name=experiment)
      if temp.count() == 0:
        exp = ExperimentModel(name=experiment, username=user,
                hit_description=desc, per_task_payment=payment,
                bonus_payment=bonus, hit_keywords=key,
                n=number_assignments, hit_title = title,
                hit_duration_in_seconds=hit_duration_in_seconds)
        exp.save()

        #create qualifications object associated w exp
        qualifications = QualificationsModel()
        qualifications.experiment = exp
        qualifications.username = user
        qualifications.save()

      else:
        # exp = ExperimentModel.objects.filter(username=user,
        #       name=experiment)[0]
        return render_to_response('createexperiment.html',
                {'experimentform': form, 'username': user,
                'duplicate': True},
                context_instance = RequestContext(request)
                )

      return HttpResponseRedirect(reverse(profile_view))
  #For non-post request:
  else :
    form = ExperimentForm(None)

  #No loading documents for list page
  return render_to_response('createexperiment.html',
          {'experimentform': form, 'username': user},
          context_instance = RequestContext(request)
          )


def CreateUserView(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    #create user object
    if form.is_valid():
      accountname = form.cleaned_data['accountname']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      key_id = form.cleaned_data['key_id']
      secret_key = form.cleaned_data['secret_key']
      #emailextension = email.split(".")[-1]
      #if not emailextension == "edu":
      #       return render_to_response('createaccounterror.html')
      #check username doesnt exist already
      match = User.objects.filter(username=accountname)
      if match.count() is 0:
        user = User.objects.create_user(accountname,email,password)
        user.save()
        researcher = Researcher(user=user, aws_key_id=key_id,
                aws_secret_key=secret_key);
        researcher.save();
      else:
        #create user form
        form = UserForm()
        user = request.user
        current_user = True
        if user.id == None:
          current_user = False
        return render_to_response('createuser.html',
                {'userform': form, 'current_user': current_user,
                 'user': user, 'duplicate': True},
                )

    #logout previous user. login new user and send them to profile
    logout(request)
    user = authenticate(username=accountname, password=password)

    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse(profile_view))
  else:
    #create user form
    form = UserForm()
    if request.user.id is not None:
      user = str(request.user)
      current_user = True
    else:
      user = False
      current_user = False
    return render_to_response('createuser.html',
            {'userform': form, 'current_user': current_user, 'user': user},
            )

def DocumentationView(request):
  if request.user.id is not None:
    user = str(request.user)
  else:
    user = False
  return render_to_response('documentation.html',
          {'current_user':user}
          )

def EditBonusPaymentView(request,username, experiment):
  if request.method == 'POST':
    form = BonusPaymentForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.bonus_payment = form.cleaned_data['bonus_payment']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - Bonus Payment Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))


def EditConfigFileNameView(request, username, experiment):
  if request.method == 'POST':
    form = ConfigFileForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.config_file = form.cleaned_data['config_file_name']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - Config File Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))


def EditHitDescriptionView(request, username, experiment):
  if request.method == 'POST':
    form = HitDescriptionForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_description = form.cleaned_data['hit_description']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - HIT Description Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def EditHitTitleView(request, username, experiment):
  if request.method == 'POST':
    form = HitTitleForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_title = form.cleaned_data['hit_title']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - HIT Title Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def EditHitDurationView(request, username, experiment):
  if request.method == 'POST':
    form = HitDurationForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_duration_in_seconds = form.cleaned_data['hit_duration_in_seconds']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - HIT Duration Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def EditHitFrameHeightView(request, username, experiment):
  if request.method == 'POST':
    form = HitFrameHeightForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_frame_height = form.cleaned_data['hit_frame_height']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - HIT Frame Height Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))


def EditHitKeywordView(request, username, experiment):
  if request.method == 'POST':
    form = HitKeywordsForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_keywords = form.cleaned_data['hit_keywords']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - HIT Keywords Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def EditLinkView(request, username, experiment):
  #creates link
  if request.method == 'POST':
    form = LinkForm(request.POST)
    if form.is_valid():
      #first check to make sure experiment exists for user.
      links_from_form = (form.cleaned_data['experiment_to_link']).split(',')
      cleaned_links = []
      for link in links_from_form:
        cleaned_links.append(link.strip())

      exps_to_link = []
      for link in cleaned_links:
        exp_to_link = GetExperiment(username, link)
        exps_to_link.append(exp_to_link)
        #if that experiment doesn't exist...
        if not exp_to_link:
          messages.add_message(request,
                  messages.SUCCESS, "The experiment " + exp_to_link + " does not exist.")
          return HttpResponseRedirect(reverse(profile_view))
        else:
          exp = GetExperiment(username, experiment)
          exp_to_link = GetExperiment(username, link)
          exp.linked_experiments = exp.linked_experiments + " " + exp_to_link.name
          exp_to_link.linked_experiments = exp_to_link.linked_experiments  + " " + exp.name
          #current_links = old_links + " " + form.cleaned_data['experiment_to_link']
          #exp.linked_experiments = current_links
          exp.save()
          exp_to_link.save()
      messages.add_message(request,
              messages.SUCCESS, "Link(s) created successfully.")
      return HttpResponseRedirect(reverse(profile_view))

      #exp = GetExperiment(username, experiment)
      #exp.per_task_payment = form.cleaned_data['per_task_payment']
      #exp.save()
  else:
    #messages.add_message(request,
    #                       messages.SUCCESS, "word.")
    return HttpResponseRedirect(reverse(profile_view))

def EditHitPaymentView(request, username, experiment):
  if request.method == 'POST':
    form = HitPaymentForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.per_task_payment = form.cleaned_data['per_task_payment']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - Per Task Payment Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))


def EditTaskNumberView(request, username, experiment):
  if request.method == 'POST':
    form = TaskNumberForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.n = form.cleaned_data['number_of_assignments']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - Number of Assignments Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def EditTaskSubmissionPaymentView(request, username, experiment):
  if request.method == "POST":
    form = TaskSubmissionPaymentForm(request.POST)
    if form.is_valid():
      exp = GetExperiment(username, experiment)
      exp.hit_submission_payment = form.cleaned_data['task_submission_payment']
      exp.save()
      messages.add_message(request,
              messages.SUCCESS, experiment + ' - Task Submission Payment Edited Successfully.')
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return HttpResponseRedirect(reverse(profile_view))

def ExperimentView(request, username, experiment):

  current_exp = GetExperiment(username, experiment)

  #check if wid had completed any linked experiments.
  current_wid = request.GET.get('workerid', '')

  #first for current experiment get list of linked experiments
  linked_exps = (current_exp.linked_experiments).split()
  linked_exps.append(current_exp.name) #this is mainly for debugging purposes

  #big wid list
  disallowed_wids = ["jj"]
  for linked_exp in linked_exps:
    #get all workertask objects with this user and experiment name
    tasks = WorkerTask.objects.filter(researcher=username, experiment__name=linked_exp)
    for task in tasks:
      disallowed_wids.append(task.wid)

  #if workerid in list of not cool worker ids
  if current_wid in disallowed_wids:
    #return page showing they are bumped
    messages.add_message(request,
                    messages.SUCCESS, "YOU FAIL " + current_wid)
    return HttpResponse("Apologies, you are ineligible to accept this HIT.")

  file_objects = current_exp.experimentfile_set.all()
  filedict = {}
  index_file_count = file_objects.filter(original_filename="index.html")
  index_file_count = index_file_count.count()
  if index_file_count == 0:
    return render_to_response('noindex.html',{"current_user": username,
            "user": username})
  index_file = str(file_objects.get(original_filename = "index.html"))
  index_file = index_file.split("/")[-1]
  #populate dictionary
  for each in file_objects:
    filedict[each.docfile] = each.filetext
    filedict[each.original_filename] = each.docfile

  return render_to_response(index_file,
          {'testfiles': filedict,  'username': username}
          )


def FileHttpResponse(request, username, experiment, filename):
  #Get proper experiment and file

  DEBUG = False

  if filename=="api.js" and DEBUG==False:

    print("\n\n\n\n TRYING TO GET THE API.")
    return render_to_response('api.js',     {'username':username,
            'experiment':experiment})


  print 'File', username, experiment, filename
  exp = GetExperiment(username, experiment)
  file_object = exp.experimentfile_set.get(original_filename = filename)
  static_content = file_object.filetext

  return (HttpResponse(content=static_content))


def LoginView(request):
  if request.method == 'POST':
    #login
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)

    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse(profile_view))

    mismatch = True
    #return loginerror is user in not active.
    return render_to_response('login.html',
            {'loginform': form, 'user': None, 'current_user': None,
            'mismatch': mismatch, 'profileerror': False,},
            )
  else:
    form = LoginForm()
    user = request.user

    current_user = True
    if user.id == None:
      current_user = False
    mismatch = False;
    return render_to_response('login.html',
            {'loginform': form, 'user': user, 'current_user': current_user,
            'mismatch': mismatch, 'profileerror': False,},
            )


def LogoutView(request):
  logout(request)
  return HttpResponseRedirect(reverse(login_view))


def ProfileGalleryView(request):
  #User authentication
  if request.user.is_authenticated:
    username = request.user

  if request.user.id is None:
    return render_to_response('login.html',
            {'loginform': LoginForm(), 'user': None, 'current_user': False,
            'mismatch': False, 'profileerror': True,},
            )

  # list of experiments for given user
  experiments_list = ExperimentModel.objects.filter(username=username)

  # fildict: Key: eexperiment.name, Value: files assocaited w/ experiment
  filedict = {}
  for experiment in experiments_list:
    file_list = []
    current_exp = experiments_list.get(name=experiment)
    #add all files associated with experiment
    for file in current_exp.experimentfile_set.all():
      file_list.append(file)
    filedict[experiment.name] = file_list

  linked_exp_dict = {}
  for experiment in experiments_list:
    links_list = []
    current_exp = experiments_list.get(name=experiment)
    #add names of all linked experiments
    #do that here
    linkstring = experiment.linked_experiments
    linked_exp_dict[experiment.name] = linkstring
    ##come here

  linkdict = {} # Dictionary of experiment links
  publishdict = {} # Dictionary of puublished values
  pub_sandbox = {} #Dictionary of sandbox values. True if posted
  q_linkdict = {} # Dictionary of links to qualifications pages
  for exp in experiments_list:
    linkdict[exp.name] ="/gpaas/experiment/"+str(username)+"/"+exp.name+"/"
    publishdict[exp.name] = exp.published_mturk
    pub_sandbox[exp.name] = exp.published_sandbox
    q_linkdict[exp.name] = "/gpaas/qualification/"+\
            str(username)+"/"+exp.name+"/"

  # if request.method != 'POST':
  #       # populate qualifications form
  #       exp = AuthenticateExperiment(username,experiment)
  #       qualifications = exp.qualificationsmodel_set
  #       # userperson = exp.username
  #       q_set = qualifications.get(username=username)

  #       form = QualificationsForm(
  #               {'us_residents_only': q_set.US_only,
  #               'percentage_hits_approved': q_set.percentage_hits_approved,
  #               'percentage_assignments_submitted':
  #                       q_set.percentage_assignments_submitted,
  #               })

  #       post_url = "/gpaas/qualification/"+username+"/"+experiment+"/"

  #       return render_to_response('qualification.html',
  #               {'qualform': form, 'user': username,
  #               'experiment':experiment, 'post_url': post_url,},
  #               )

  #Populate formdict {'experiment.name':{'FormName': form, ... }, ...}
  formdict = {}
  for exp in experiments_list:
    inner_formdict = {}

    #main experiment forms
    inner_formdict["hit_description_form"] = HitDescriptionForm(
            {'hit_description': exp.hit_description}).as_p()
    inner_formdict["hit_payment_form"] = HitPaymentForm(
            {'per_task_payment': exp.per_task_payment}).as_p()
    inner_formdict["bonus_payment_form"] = BonusPaymentForm(
            {'bonus_payment': exp.bonus_payment}).as_p()
    inner_formdict["task_submission_payment_form"] = TaskSubmissionPaymentForm(
            {'task_submission_payment':exp.hit_submission_payment}).as_p()
    inner_formdict["hit_keywords_form"] = HitKeywordsForm(
            {'hit_keywords': exp.hit_keywords}).as_p()
    inner_formdict["tasknumber_form"] = TaskNumberForm(
            {'number_of_assignments': exp.n}).as_p()
    inner_formdict["config_file_form"] = ConfigFileForm(
            {'config_file_name': exp.config_file}).as_p()
    inner_formdict["hit_duration_form"] = HitDurationForm(
            {'hit_duration_in_seconds': exp.hit_duration_in_seconds}).as_p()
    inner_formdict["hit_title_form"] = HitTitleForm(
            {'hit_title': exp.hit_title}).as_p()
    inner_formdict["hit_frame_height_form"] = HitFrameHeightForm(
            {'hit_frame_height': exp.hit_frame_height}).as_p()

    #linkform
    inner_formdict["link_form"] = LinkForm().as_p()

    #qualifications form
    qualifications = exp.qualificationsmodel_set
    q_set = qualifications.get(username=username)
    inner_formdict["qualification_form"] = QualificationsForm(
            {'us_residents_only': q_set.US_only,
            'percentage_hits_approved': q_set.percentage_hits_approved,
            'percentage_assignments_submitted': q_set.percentage_assignments_submitted,
            }).as_p()

    #add inner_formdict to outer formdict
    formdict[exp.name] = inner_formdict

  #No loading documents for list page
  return render_to_response('profilegallery.html',
          {'username': username, 'experiments_list': experiments_list,
          # dictionaries
          'filedict': filedict, 'linkdict': linkdict, 'q_linkdict': q_linkdict,
          'publishdict': publishdict, 'pub_sandbox':pub_sandbox,
          'formdict': formdict, 'linked_exp_dict':linked_exp_dict,
          # Form urls:
                  # Use in template: {{url_base}}{{experiment}}{{specific}}
          'bonus_payment_url'   : "/bonuspayment/",
          'hit_description_url' : "/hitdescription/",
          'hit_keywords_url'    : "/hitkeywords/",
          'hit_payment_url'     : "/hitpayment/",
          'hit_title_url'       : "/hittitle/",
          'hit_frame_height_url': "/hitframeheight/",
          'hit_duration_url'    : "/hitduration/",
          'submit_payment_url'  : "/submitpayment/",
          'sandbox_url'         : "/sandbox/",
          'tasknumber_url'      : "/tasknumber/",
          'link_url'                        : "/link/",
          'upload_url'          : "/",
          'config_url'              : "/config/",
          'url_base'            : "/gpaas/edit/"+str(username)+"/",
          'uploadform'          : UploadForm(),
          },
          context_instance = RequestContext(request)
          )


def QualificationView(request, username, experiment):
  if request.method != 'POST':
    # populate qualifications form
    exp = AuthenticateExperiment(username,experiment)
    qualifications = exp.qualificationsmodel_set
    # userperson = exp.username
    q_set = qualifications.get(username=username)

    form = QualificationsForm(
            {'us_residents_only': q_set.US_only,
            'percentage_hits_approved': q_set.percentage_hits_approved,
            'percentage_assignments_submitted':
                    q_set.percentage_assignments_submitted,
            })

    post_url = "/gpaas/qualification/"+username+"/"+experiment+"/"

    return render_to_response('qualification.html',
            {'qualform': form, 'user': username,
            'experiment':experiment, 'post_url': post_url,},
            )
  else:
    user = AuthenticateUser(request)
    exp = GetExperiment(username, experiment)
      # exp = ExperimentModel.objects.filter(username=username)
      # return exp.get(name=experiment)
    qualifications = QualificationsModel.objects.get(experiment=exp)
    form = QualificationsForm(request.POST)
    # form = ExperimentForm(request.POST, request.FILES)
    #Update experiment qualifications
    if form.is_valid():
      # adult = form.cleaned_data['adult_requirement']
      print("\n" + str(form.cleaned_data['us_residents_only']) + "\n")
      qualifications.US_only = form.cleaned_data['us_residents_only']
      # percentage_appr = form.cleaned_data['percentage_hits_approved']
      qualifications.percentage_hits_approved = (
              form.cleaned_data['percentage_hits_approved'])
      # percentage_subm = form.cleaned_data['percentage_assignments_submitted']
      qualifications.percentage_assignments_submitted = (
              form.cleaned_data['percentage_assignments_submitted'])
      qualifications.save()

    return HttpResponseRedirect(reverse(profile_view))


def UploadView(request, username, experiment):
  logger.info("/UploadView")
  if request.method != 'POST':
    logger.info("Method was GET.  rejected")
    return HttpResponseRedirect(reverse(profile_view))
  else:
    user = AuthenticateUser(request)
    exp = AuthenticateExperiment(username, experiment)
    form = UploadForm(request.POST, request.FILES)

    #Create ExperimentFile instance for each uploaded file.
    logger.info("Checking if form is valid: %s" % form.is_valid())
    if form.is_valid():
      for each in request.FILES.getlist('attachments'):
        # if file exists, delete old instance.
        try:
          plain_filename = str(each).split('/')[-1]
          duplicate = ExperimentFile.objects.filter(username=user)
          duplicate = duplicate.filter(experiment=exp)
          duplicate =duplicate.get(original_filename=plain_filename)
          #remove physical file
          try:
            os.remove(settings.BASE_DIR +"/expdeploy/"+
                    str(duplicate.docfile))
          except OSError:
            pass
          duplicate.delete()
        except ExperimentFile.DoesNotExist:
          duplicate = None

        #create new ExperimentFile object
        newdoc = ExperimentFile(
            original_filename=each,
            docfile=each,
            username=user,
            filetext="tmptxt")

        logger.info("created new file %s at %s" % (each, newdoc.docfile.path))
        newdoc.experiment = exp
        newdoc.save()

        #Open document to read contents and save to filetext field
        f = open(newdoc.docfile.path, "r")
        file_contents = f.read()
        newdoc.filetext = file_contents
        newdoc.save()

      return HttpResponseRedirect(reverse(profile_view))
    else:
      return HttpResponseRedirect(reverse(profile_view))

def WelcomeView(request):
  if request.user.id is not None:
    return HttpResponseRedirect(reverse(profile_view))
  else:
    return render_to_response('welcome.html')

def WelcomeDirectView(request):
  if request.user.id is not None:
    user = str(request.user)
  else:
    user = False
  return render_to_response('welcome.html',
          {'current_user':user}
          )
