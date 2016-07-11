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
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/hitdescription/$', 'EditHitDescriptionView', name='hit_description'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/hitpayment/$', 'EditHitPaymentView', name='hit_payment'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/bonuspayment/$', 'EditBonusPaymentView', name='bonus_payment'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/submitpayment/$', 'EditTaskSubmissionPaymentView', name='submit_payment'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/hitkeywords/$', 'EditHitKeywordView', name='hit_keyword'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/tasknumber/$', 'EditTaskNumberView', name='task_number'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/config/$', 'EditConfigFileNameView', name='config_file'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/$', 'UploadView', name='upload'),

    # experiment view
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/$', 'ExperimentView', name='experiment_page'),

    # HttpResponses to serve static files
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/(?P<filename>[A-Za-z0-9\w,-._]+)/$', 'FileHttpResponse', name='file_http_response'),
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/(?P<filename>[A-Za-z0-9\w.,-_]+)$', 'FileHttpResponse', name='file_http_response'),
    
    # login and logout
    url(r'^login/$', 'LoginView', name='login'),
    url(r'^logout/$', 'LogoutView', name='logout'),

    url(r'^qualification/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-_]+)/$', 'QualificationView', name='qualification'),

    url(r'^profile/$', 'ProfileGalleryView', name='user_profile'),
    url(r'^$', 'WelcomeView', name="welcome"),
    url(r'^welcome/$', 'WelcomeDirectView', name="welcome_direct"),
)
