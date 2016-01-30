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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from .models import ExperimentFile
from .forms import UploadForm

def UploadView(request):
	#Upload files for post request
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		#Create ExperimentFile instance for each uploaded file.
		if form.is_valid():
			user = form.cleaned_data['username']
			for each in request.FILES.getlist("attachments"):
				newdoc = ExperimentFile(docfile=each, username=user)
				newdoc.save()
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
