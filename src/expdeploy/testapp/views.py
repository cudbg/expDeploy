# -*- coding: utf-8 -*-
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings 

from .models import ExperimentFile
from .forms import UploadForm
from django.contrib.auth.models import User
from .forms import UserForm

import os
import json
import sys

from expdeploy.api.models import Experiment

def UserProfileView(request):
	return render_to_response('userprofile.html')

def CreateUser(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		#create user object
		if form.is_valid():
			accountname = form.cleaned_data['accountname']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			user = User.objects.create_user(accountname,email,password)		
			user.save()		
		#return to user page
		return HttpResponseRedirect(reverse('expdeploy.testapp.views.UserProfileView'))
	else:
		#create user form
		form = UserForm()
		return render_to_response('createuser.html',
			{'userform': form},
			context_instance = RequestContext(request)
		)

def UploadView(request):
	#Upload files for post request
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():
			user = form.cleaned_data['username']
			for each in request.FILES.getlist("attachments"):
				# if instance of file for this user exists already, delete old instance.
				try: 
					plain_filename = str(each).split('/')[-1]
					duplicate = ExperimentFile.objects.filter(username=user).get(original_filename=plain_filename)
					#remove physical file
					try:
						os.remove(settings.BASE_DIR +"/expdeploy/"+str(duplicate.docfile))
					except OSError:
						pass
					duplicate.delete()
				except ExperimentFile.DoesNotExist:
					duplicate = None
				#create new ExperimentFile object
				newdoc = ExperimentFile(original_filename=each, docfile=each,username=user, filetext="tmptxt")
				newdoc.save()
				
				#Open document to read contents and save to filetext field
				f = open(newdoc.docfile.path, "r")
  				file_contents = f.read()
  				newdoc.filetext = file_contents
  				newdoc.save()
				# if (str(each).strip() == "config.json"):
				# 	print("GOT THE CONFIG FILE");
				# 	s = each.read().decode('utf-8')
				# 	j = json.loads(s);
				# 	exps = Experiment.objects.filter(name=j["experimentId"], researcher_id=j["userID"]);
				# 	e = None;
				# 	if len(exps) == 0:
				# 		e = Experiment(name=j["experimentId"], researcher_id=j["userID"]);
				# 		print("--Created new experiment--")
				# 	else:
				# 		print("--Modified config of old experiment--");
				# 		e = exps[0];
					
				# 	e.data = json.dumps(j);
				# 	e.save();
				#else:
					#ask hamed about this bit later.
					#newdoc = ExperimentFile(docfile=each, username=user)
					#newdoc.save()
				#print(each)

			return HttpResponseRedirect(reverse('expdeploy.testapp.views.UploadView'))
	#For non-post request:
	else :
		form = UploadForm()

	#No loading documents for list page
	return render_to_response('uploadpage.html',
		{'uploadform': form},
		context_instance = RequestContext(request)
	)

def ExperimentView(request, username):
	file_objects = ExperimentFile.objects.filter(username = username)
	filedict = { '1234567890' : None}
	index_file = str(file_objects.get(original_filename = "index.html"))
	index_file = index_file.split("/")[-1]
	#populate dictionary
	for each in file_objects:
		filedict[each.docfile] = each.filetext
		filedict[each.original_filename] = each.docfile

	return render_to_response(index_file,
		{'testfiles': filedict,  'username': username}
	)
