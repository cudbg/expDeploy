from django.conf.urls import patterns, url
from .views import UploadView

urlpatterns = patterns(
    'expdeploy.testapp.views',
    url(r'^$', 'UploadView', name='uploaaaaaaaad'),
    url(r'^experiment/$', 'ExperimentView', name='Huzzah!'),
    #Dynamics URLS to come later
)
