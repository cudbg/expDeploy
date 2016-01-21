from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from expdeploy.imageloader.models import Image
from expdeploy.imageloader.forms import ImageForm

def gallery(request):
	# Handle image upload
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            newimg = Image(imgfile = request.FILES['imgfile'])
            newimg.save()

            # Redirect to the image gallery after POST
            return HttpResponseRedirect(reverse('expdeploy.imageloader.views.gallery'))
    else:
        form = ImageForm() #empty form, adds nothing

    # Load images for the gallery
    gallery_images = Image.objects.all()

    # Render list page with the pictures and the form
    return render_to_response('gallery.html',
        {'gallery_images': gallery_images, 'form': form},
        context_instance=RequestContext(request)
    )