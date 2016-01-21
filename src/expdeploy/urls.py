from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fileloader/', include('expdeploy.fileloader.urls')),
    url(r'^imageloader/', include('expdeploy.imageloader.urls')),
    url(r'^planout_test/', include('expdeploy.planout_test.urls')),
    url(r'^templateloader/', include('expdeploy.templateloader.urls')),
    url(r'^$', RedirectView.as_view(url='/myapp/list/', permanent=True)),
    #SOME JANK
    url(r'^myapp/list/', RedirectView.as_view(url = "/fileloader/list/", permanent = True)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
