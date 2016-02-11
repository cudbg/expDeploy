# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

# views.py
"""
from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import ExperimentFile
class UploadView(FormView):
    template_name = 'uploadpage.html'
    form_class = UploadForm
    success_url = '/done/'
    def form_valid(self, form):
    	#create ExperimentFiel instance for each file uploaded.
    	user = form.cleaned_data['username']
        for each in form.cleaned_data['attachments']:
            ExperimentFile.objects.create(docfile=each, username = user)
        return super(UploadView, self).form_valid(form)
        """
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from .models import ExperimentFile
from .forms import UploadForm

import json
import sys

from expdeploy.api.models import Experiment

def UploadView(request):
	#Upload files for post request
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():
			user = form.cleaned_data['username']
			for each in request.FILES.getlist("attachments"):
<<<<<<< HEAD
				#Empty file_contents at first, then open and read file
				newdoc = ExperimentFile(docfile=each, username=user, filetext = "boop")
				newdoc.save()
				
				#Open document to read contents and save to filetext field
				f = open(newdoc.docfile.path, "r")
  				file_contents = f.read()
  				newdoc.filetext = file_contents
  				newdoc.save()
=======
				if (str(each).strip() == "config.json"):
					print("GOT THE CONFIG FILE");
					s = each.read().decode('utf-8')
					j = json.loads(s);
					exps = Experiment.objects.filter(name=j["experimentId"], researcher_id=j["userID"]);
					e = None;
					if len(exps) == 0:
						e = Experiment(name=j["experimentId"], researcher_id=j["userID"]);
						print("--Created new experiment--")
					else:
						print("--Modified config of old experiment--");
						e = exps[0];
					
					e.data = json.dumps(j);
					e.save();
				else:
					newdoc = ExperimentFile(docfile=each, username=user)
					newdoc.save()
				#print(each)
>>>>>>> 2ecdf8c633c0f806d514884057eff1ed87bec1f2

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
	#When dynamic urls added: need username based on url. see: HttpRequest.path
	filedict = { '1234567890' : None}
	for each in ExperimentFile.objects.all():
		filedict[each.docfile] = each.filetext
	#testfile = ExperimentFile.objects.get(docfile ="testapp/webfiles/hello.js").filetext
	return render_to_response('index.html',
		{'testfiles': filedict,  'username': username}
	)