# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from expdeploy.fileloader.models import Document
from expdeploy.fileloader.forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('expdeploy.fileloader.views.list'))
    else:
        form = DocumentForm()  # empty form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response('list.html',
        {'documents': documents, 'form': form},
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