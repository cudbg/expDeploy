from django.conf.urls import patterns, url
from .views import UploadView

urlpatterns = patterns(
    'expdeploy.testapp.views',
    url(r'^$', 'UploadView', name='uploaaaaaaaad'),
    #url(r'^experiment/$', 'ExperimentView', name='Huzzah!'),
    #Dynamics URLS to come later
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/$', 'ExperimentView', name='Huzzah!'),
)