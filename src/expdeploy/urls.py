from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [

	url(r'^$', RedirectView.as_view(url='/gpaas/', permanent=False)),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('expdeploy.api.urls')),
	url(r'^gpaas/', include('expdeploy.gpaas.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.autodiscover() 