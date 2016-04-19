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

    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/(?P<filename>[A-Za-z0-9\w.]+)/$',\
        'FileHttpResponse', name='file_http_response'),
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/(?P<filename>[A-Za-z0-9\w.]+)$',\
        'FileHttpResponse', name='file_http_response'),
    

    url(r'^$', 'LoginView', name='login'),
    url(r'^logout/$', 'LogoutView', name='logout'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/$', 'UploadFileView', name='upload'),

    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/hitdescription/$', 'EditHitDescriptionView', name='hit_description'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/hitpayment/$', 'EditHitPaymentView', name='hit_payment'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/hitkeywords/$', 'EditHitKeywordView', name='hit_keyword'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/sandbox/$', 'EditSandboxView', name='sandbox'),
    url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9]+)/tasknumber/$', 'EditTaskNumberView', name='task_number'),

    url(r'^userprofile/$', 'UserProfileView', name='user_profile'),
)