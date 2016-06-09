# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings 

from .models import ExperimentFile, ExperimentModel, QualificationsModel
from django.contrib.auth.models import User
from .models import Researcher

from .forms import LoginForm, UploadForm, UserForm, ExperimentForm,\
	QualificationsForm
from .forms import HitDescriptionForm, HitPaymentForm, \
	HitKeywordsForm, SandboxForm, TaskNumberForm, BonusPaymentForm

import os
import json
import sys

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
	return exp.get(name=experiment)


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
			bonus = form.cleaned_data['bonus_payment']
			key = form.cleaned_data['hit_keywords']

			#check if experiment already exists
			temp = ExperimentModel.objects.filter(username=user)
			temp = temp.filter(name=experiment)
			if temp.count() == 0:
			 	exp = ExperimentModel(name=experiment, username=user,
			 		hit_description=desc, per_task_payment=payment,
			 		bonus_payment=bonus, hit_keywords=key)
				exp.save()

				#create qualifications object associated w exp
				qualifications = QualificationsModel()
				qualifications.experiment = exp
				qualifications.username = user
				qualifications.save()

			else: 
				# exp = ExperimentModel.objects.filter(username=user,
				# 	name=experiment)[0]
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
			#	return render_to_response('createaccounterror.html')
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
		user = request.user
		current_user = True
		if user.id == None:
		 	current_user = False
		return render_to_response('createuser.html',
			{'userform': form, 'current_user': current_user, 'user': user},
			)


def EditBonusPaymentView(request,username, experiment):
	if request.method == 'POST':
		form = BonusPaymentForm(request.POST)
		if form.is_valid():
			exp = GetExperiment(username, experiment)
			exp.bonus_payment = form.cleaned_data['bonus_payment']
			exp.save()
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
		return HttpResponseRedirect(reverse(profile_view))
	else:
		return HttpResponseRedirect(reverse(profile_view))


def EditHitKeywordView(request, username, experiment):
	if request.method == 'POST':
		form = HitKeywordsForm(request.POST)
		if form.is_valid():
			exp = ExperimentModel.objects.filter(username=username)

			exp.hit_keywords = form.cleaned_data['hit_keywords']
			exp.save()
		return HttpResponseRedirect(reverse(profile_view))
	else:
		return HttpResponseRedirect(reverse(profile_view))


def EditHitPaymentView(request, username, experiment):
	if request.method == 'POST':
		form = HitPaymentForm(request.POST)
		if form.is_valid():
			exp = GetExperiment(username, experiment)
			exp.hit_payment = form.cleaned_data['per_task_payment']
			exp.save()
		return HttpResponseRedirect(reverse(profile_view))
	else:
		return HttpResponseRedirect(reverse(profile_view))


def EditSandboxView(request, username, experiment):
	if request.method == 'POST':
		form = SandboxForm(request.POST)
		if form.is_valid():
			exp = GetExperiment(username, experiment)
			exp.sandbox = form.cleaned_data['sandbox']
			exp.save()
		return HttpResponseRedirect(reverse(profile_view))
	else:
		return HttpResponseRedirect(reverse(profile_view))


def EditTaskNumberView(request, username, experiment):
	if request.method == 'POST':
		form = TaskNumberForm(request.POST)
		if form.is_valid():
			exp = GetExperiment(username, experiment)
			exp.n = form.cleaned_data['number_of_hits']
			exp.save()
		return HttpResponseRedirect(reverse(profile_view))
	else:
		return HttpResponseRedirect(reverse(profile_view))


def ExperimentView(request, username, experiment):
	current_exp = GetExperiment(username, experiment)
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

	#  populate linkdict and publisheddict
	linkdict = {} # Dictionary of experiment links
	publishdict = {} # Dictionary of puublished values
	q_linkdict = {} # Dictionary of links to qualifications pages
	for exp in experiments_list:
		linkdict[exp.name] ="/gpaas/experiment/"+str(username)+"/"+exp.name+"/"
		publishdict[exp.name] = exp.published
		q_linkdict[exp.name] = "/gpaas/qualification/"+\
			str(username)+"/"+exp.name+"/"


	#Populate formdict {'experiment.name':{'FormName': form, ... }, ...}
	formdict = {}
	for exp in experiments_list:
		inner_formdict = {}
		inner_formdict["hit_description_form"] = HitDescriptionForm(
			{'hit_description': exp.hit_description}).as_p()
		inner_formdict["hit_payment_form"] = HitPaymentForm(
			{'per_task_payment': exp.per_task_payment}).as_p()
		inner_formdict["bonus_payment_form"] = BonusPaymentForm(
			{'bonus_payment': exp.bonus_payment}).as_p()
		inner_formdict["hit_keywords_form"] = HitKeywordsForm(
			{'hit_keywords': exp.hit_keywords}).as_p()
		inner_formdict["sandbox_form"] = SandboxForm(
			{'sandbox': exp.sandbox}).as_p()
		inner_formdict["tasknumber_form"] = TaskNumberForm(
			{'number_of_hits': exp.n}).as_p()
		#add inner_formdict to outer formdict
		formdict[exp.name] = inner_formdict

	#No loading documents for list page
	return render_to_response('profilegallery.html',
		{'username': username, 'experiments_list': experiments_list, 
		# dictionaries
		'filedict': filedict, 'linkdict': linkdict, 'q_linkdict':q_linkdict,
		'publishdict': publishdict, 'formdict': formdict,
		# Form urls:
			# Use in template: {{url_base}}{{experiment}}{{specific}}
		'bonus_payment_url'   : "/bonuspayment/", 
		'hit_description_url' : "/hitdescription/",
		'hit_keywords_url'    : "/hitkeywords/", 
		'hit_payment_url'     : "/hitpayment/",
		'sandbox_url'         : "/sandbox/", 
		'tasknumber_url'      : "/tasknumber/",
		'upload_url'          : "/",
		'url_base'            : "/gpaas/edit/"+str(username)+"/", 
		# forms
		'uploadform'          : UploadForm(),
		'bonus_payment_form'  : BonusPaymentForm(),
		'hit_description_form': HitDescriptionForm(),
		'hit_payment_form'    : HitPaymentForm(),
		'hit_keywords_form'   : HitKeywordsForm(), 
		'sandbox_form'        : SandboxForm(), 
		'tasknumber_form'     : TaskNumberForm(),},
		context_instance = RequestContext(request)
		)


def QualificationView(request, username, experiment):
	if request.method != 'POST':
		# populate qualifications form
		exp = AuthenticateExperiment(username,experiment)
		qualifications = exp.qualificationsmodel_set
		userperson = exp.username
		q_set = qualifications.get(username=username)

		form = QualificationsForm(
			{'adult_requirement': q_set.adult_requirement,
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
		exp = AuthenticateExperiment(username, experiment)
		form = QualificationsForm(request.POST, request.FILES)
		form = ExperimentForm(request.POST, request.FILES)
		#Update experiment qualifications
		if form.is_valid():
			exp.adult_requirement = form.cleaned_data['adult_requirement']
			exp.percentage_hits_approved = (
				form.cleaned_data['percentage_hits_approved'])
			exp.percentage_assigments_submitted = (
				form.cleaned_data['percentage_assignments_submitted'])
			exp.save()
		return HttpResponseRedirect(reverse(profile_view))


def UploadView(request, username, experiment):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse(profile_view))
	else:
		user = AuthenticateUser(request)
		exp = AuthenticateExperiment(username, experiment)
		form = UploadForm(request.POST, request.FILES)

		#Create ExperimentFile instance for each uploaded file.
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
				newdoc = ExperimentFile(original_filename=each,\
					docfile=each,username=user, filetext="tmptxt")

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