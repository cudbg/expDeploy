# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings 

from .models import ExperimentFile
from .models import ExperimentModel
from django.contrib.auth.models import User
from .models import Researcher

from .forms import LoginForm
from .forms import UploadForm
from .forms import UserForm
from .forms import ExperimentForm

import os
import json
import sys


def CreateExperimentView(request):
	#user
	if request.user.is_authenticated: 
			user = str(request.user)
	else: 
			user = None
	if request.user.id is None:
		return render_to_response('profileerror.html')

	#Upload files for post request
	if request.method == 'POST':
		form = ExperimentForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():
			#get experiment
			experiment = form.cleaned_data['experiment']
			#if experiment already exists, use it. If not, make a new one.

			#check if experiment already exists
			temp = ExperimentModel.objects.filter(username=user).filter(name=experiment)
			if not temp:
			 	exp = ExperimentModel(name=experiment, username=user)
				exp.save()
			else: 
				exp = ExperimentModel.objects.filter(username=user,name=experiment)[0]

			return HttpResponseRedirect(reverse('expdeploy.gpaas.views.UserProfileView'))
	#For non-post request:
	else :
		form = ExperimentForm()

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
			emailextension = email.split(".")[-1]
			if not emailextension == "edu":
				return render_to_response('createaccounterror.html')
			#check username doesnt exist already
			match = ExperimentFile.objects.filter(username=accountname)
			if not match.exists():
				user = User.objects.create_user(accountname,email,password)		
			 	user.save()
			 	researcher = Researcher(user=user, aws_key_id=key_id, aws_secret_key=secret_key);
			 	researcher.save();		
			else: 
			 	return render_to_response('createaccounterror.html')
		#logout previous user. login new user and send them to profile
		logout(request)
		user = authenticate(username=accountname, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse(
					'expdeploy.gpaas.views.UserProfileView'))
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


def ErrorView(request):
	return HttpResponseRedirect(reverse('expdeploy.gpaas.views.LoginView'))


def ExperimentView(request, username, experiment):
	current_exp = ExperimentModel.objects.filter(username=username).get(name=experiment)
	file_objects = current_exp.experimentfile_set.all()
	filedict = {}
	index_file = str(file_objects.get(original_filename = "index.html"))
	index_file = index_file.split("/")[-1]
	#populate dictionary
	for each in file_objects:
		filedict[each.docfile] = each.filetext
		filedict[each.original_filename] = each.docfile

	return render_to_response(index_file,
		{'testfiles': filedict,  'username': username}
	)


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
				return HttpResponseRedirect(reverse(
					'expdeploy.gpaas.views.UserProfileView'))
		#return loginerror is user in not active.	
		return render_to_response('loginerror.html')
	else:
		form = LoginForm()
		user = request.user

		current_user = True
		if user.id == None:
		 	current_user = False
		return render_to_response('login.html',
			{'loginform': form, 'user': user, "current_user": current_user},
		)


def LogoutView(request):
	logout(request)
	return HttpResponseRedirect(reverse('expdeploy.gpaas.views.LoginView'))


def UploadFileView(request, username, experiment):

	#user
	if request.user.is_authenticated: 
			user = str(request.user)
	else: 
			user = None
	if request.user.id is None:
		return render_to_response('profileerror.html')

	#if experiment doesn't exist, return error page
	temp = ExperimentModel.objects.filter(username=user).filter(name=experiment)
	if not temp:
		return render_to_response('uploaderror.html')
	else: 
		exp = ExperimentModel.objects.filter(username=user,name=experiment)[0]

	#url
	thisurl = "/gpaas/upload/" + username + "/" + experiment + "/"

	#list of experiments
	experiment_object = ExperimentModel.objects.filter(username=username).get(name=experiment)

	#assign experiment with files
	filedict = {}
	file_list = []
	#add all files associated with experiment
	for file in experiment_object.experimentfile_set.all():
		file_list.append(file)
	filedict[experiment_object] = file_list

	#create experiment links in dict form
	linkdict = {}
	usr = str(username)
	linkdict[experiment] = "/gpaas/experiment/"+usr+"/"+experiment+"/"

	#Uploadfiles for post request
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():

			for each in request.FILES.getlist('attachments'):
				# if instance of file for this user exists already, delete old instance.
				try: 
					plain_filename = str(each).split('/')[-1]
					duplicate = ExperimentFile.objects.filter(username=user).\
						filter(experiment=exp).get(original_filename=plain_filename)
					#remove physical file
					try:
						os.remove(settings.BASE_DIR +"/expdeploy/"+str(duplicate.docfile))
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

			return HttpResponseRedirect(reverse('expdeploy.gpaas.views.UserProfileView'))
  			
	else :
		form = UploadForm()

	#No loading documents for list page
	return render_to_response('uploadpage.html',
		{'uploadform': form, 'username': user, 'thisurl': thisurl, 'experiments': experiment,
		'filedict': filedict,'linkdict': linkdict,},
		context_instance = RequestContext(request)
	)


def UserProfileView(request):
	if request.user.is_authenticated: 
		username = request.user
	if request.user.id is None:
		return render_to_response('profileerror.html')

	#list of experiments
	experiment_objects = ExperimentModel.objects.filter(username=username)
	experiments = []
	for each in experiment_objects:
		experiments.append(each.name)
	#make sure no duplicates
	experiments = list(set(experiments))

	#assign each experiment with related files in filedict
	filedict = {}
	#file_objects = ExperimentFile.objects.filter(username=username)
	for each in experiments:
		file_list = []
		current_exp = experiment_objects.get(name=each)
		#add all files associated with experiment
		for file in current_exp.experimentfile_set.all():
			file_list.append(file)
		filedict[each] = file_list

	#create experiment links in dict form
	linkdict = {}
	for experiment in experiments:
		#add experimenturl to first item in file_list
		usr = str(username)
		linkdict[experiment] = "/gpaas/experiment/"+usr+"/"+experiment+"/"

	#edit links
	editdict = {}
	for experiment in experiments:
		editdict[experiment] = "/gpaas/upload/"+str(username)+"/"+experiment+"/"

	#dictionary listing files in experiment
	return render_to_response('userprofile.html',
		{'username':username, 'experiments': experiments, 'filedict': filedict,
		'linkdict': linkdict, 'editdict': editdict,}
		)



def UploadView(request, experiment):
	#user
	if request.user.is_authenticated: 
			user = str(request.user)
	else: 
			user = None
	if request.user.id is None:
		return render_to_response('profileerror.html')

	#Upload files for post request
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():
			#get experiment
			experiment = form.cleaned_data['experiment']
			#if experiment already exists, use it. If not, make a new one.

			#check if experiment already exists
			temp = ExperimentModel.objects.filter(username=user).filter(name=experiment)
			if not temp:
			 	exp = ExperimentModel(name=experiment, username=user)
				exp.save()
			else: 
				exp = ExperimentModel.objects.filter(username=user,name=experiment)[0]

			for each in request.FILES.getlist('attachments'):
				# if instance of file for this user exists already, delete old instance.
				try: 
					plain_filename = str(each).split('/')[-1]
					duplicate = ExperimentFile.objects.filter(username=user).\
						filter(experiment=exp).get(original_filename=plain_filename)
					#remove physical file
					try:
						os.remove(settings.BASE_DIR +"/expdeploy/"+str(duplicate.docfile))
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

			return HttpResponseRedirect(reverse('expdeploy.gpaas.views.UserProfileView'))
	#For non-post request:
	else :
		form = UploadForm()

	#No loading documents for list page
	return render_to_response('uploadpage.html',
		{'uploadform': form, 'username': user},
		context_instance = RequestContext(request)
	)