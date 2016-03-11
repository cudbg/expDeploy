from django.conf.urls import patterns, url
from .views import UploadView

urlpatterns = patterns(
    'expdeploy.gpaas.views',

    url(r'^createuser/$', 'CreateUserView', name='create_user'),
    url(r'^createexperiment/$', 'CreateExperimentView'),
    url(r'^error/$', 'ErrorView', name='error'),

    #username and experiment name passed to view from url.
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/$',\
        'ExperimentView', name='experiment_page'),

    url(r'^$', 'LoginView', name='login'),
    url(r'^logout/$', 'LogoutView', name='logout'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/$', 'UploadFileView', name='upload'),
    url(r'^userprofile/$', 'UserProfileView', name='user_profile'),
)