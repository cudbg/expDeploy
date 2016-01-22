# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from expdeploy.fileloader.models import Document

from expdeploy.fileloader.forms import DocumentForm
from expdeploy.fileloader.forms import AttachmentForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
       # print(request.FILES);
        form = DocumentForm(request.POST, request.FILES);
        form2 = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
          #  print(request.FILES);

            for each in request.FILES.getlist("attachments"):
                newdoc = Document(docfile=each);
                newdoc.save();
                print(each);
                #return super(UploadView, self).form_valid(form)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('expdeploy.fileloader.views.list'))
    else:
        form = DocumentForm()  # empty form

    # Load documents for the list page
    documents = Document.objects.all()
    attachments = AttachmentForm();
    # Render list page with the documents and the form
    return render_to_response('list.html',
        {'documents': documents, 'form': form, 'attachments':attachments},
        context_instance=RequestContext(request)
    )

def delete(request):
    if request.method != 'POST':
        raise Http404("Method: " + request.method +". Cannot access URL directly.")

    # Load documents for the list page
    documents = Document.objects.all()
    for document in documents:
        document.delete()

    # Redirect to the blank list after deletion
    return HttpResponseRedirect(reverse('expdeploy.fileloader.views.list'))