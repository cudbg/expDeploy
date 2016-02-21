from django.conf.urls import patterns, url
from .views import UploadView

urlpatterns = patterns(
    'expdeploy.testapp.views',

    #upload and experiment views
    url(r'^$', 'UploadView', name='upload'),
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/$', 'ExperimentView', name='experiment_page'),

   	#createuser form and user profiles
    url(r'^createuser/$', "CreateUserView", name='create_user'),
    url(r'^userprofile/(?P<username>[A-Za-z0-9]+)/$', 'UserProfileView', name ='user_profile'),
)