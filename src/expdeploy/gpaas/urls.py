from django.conf.urls import patterns, url
#from .views import UploadFileView


urlpatterns = patterns(
    'expdeploy.gpaas.views',
    #view results go here, not at the bottom???
    url(r'^viewresults', 'ViewResults', name='ViewResults'),

    url(r'^createuser/$', 'CreateUserView', name='create_user'),
    url(r'^createexperiment/$', 'CreateExperimentView'),
    url(r'^documentation/$', 'DocumentationView'),
    
    # username and experiment name passed to view from url.
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/hitdescription/$', 'EditHitDescriptionView', name='hit_description'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/hitpayment/$', 'EditHitPaymentView', name='hit_payment'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/bonuspayment/$', 'EditBonusPaymentView', name='bonus_payment'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/submitpayment/$', 'EditTaskSubmissionPaymentView', name='submit_payment'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/hitkeywords/$', 'EditHitKeywordView', name='hit_keyword'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/tasknumber/$', 'EditTaskNumberView', name='task_number'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/config/$', 'EditConfigFileNameView', name='config_file'),
    url(ur'^edit/(?P<username>[-\w]+)/(?P<experiment>.*)/$', 'UploadView', name='upload'),

    # experiment view
    url(ur'^experiment/(?P<username>[-\w]+)/(?P<experiment>.*)/$', 'ExperimentView', name='experiment_page'),

    # HttpResponses to serve static files
    url(ur'^experiment/(?P<username>[-\w]+)/(?P<experiment>.*)/(?P<filename>.*)/$', 'FileHttpResponse', name='file_http_response'),
    url(ur'^experiment/(?P<username>[-\w]+)/(?P<experiment>.*)/(?P<filename>.*)$', 'FileHttpResponse', name='file_http_response'),
    
    # login and logout
    url(r'^login/$', 'LoginView', name='login'),
    url(r'^logout/$', 'LogoutView', name='logout'),

    url(ur'^qualification/(?P<username>[-\w]+)/(?P<experiment>.*)/$', 'QualificationView', name='qualification'),

    url(r'^profile/$', 'ProfileGalleryView', name='user_profile'),
    url(r'^$', 'WelcomeView', name="welcome"),
    url(r'^welcome/$', 'WelcomeDirectView', name="welcome_direct"),
)
