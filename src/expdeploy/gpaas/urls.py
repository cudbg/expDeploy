from django.conf.urls import patterns, url
#from .views import UploadFileView

urlpatterns = patterns(
    'expdeploy.gpaas.views',

    url(r'^createuser/$', 'CreateUserView', name='create_user'),
    url(r'^createexperiment/$', 'CreateExperimentView'),
    
    # username and experiment name passed to view from url.
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitdescription/$', 'EditHitDescriptionView', name='hit_description'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitpayment/$', 'EditHitPaymentView', name='hit_payment'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/bonuspayment/$', 'EditBonusPaymentView', name='bonus_payment'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitkeywords/$', 'EditHitKeywordView', name='hit_keyword'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/sandbox/$', 'EditSandboxView', name='sandbox'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/tasknumber/$', 'EditTaskNumberView', name='task_number'),
    url(r'^edit/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/$', 'UploadView', name='upload'),

    # experiment view
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/$', 'ExperimentView', name='experiment_page'),

    # HttpResponses to serve static files
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/(?P<filename>[A-Za-z0-9\w,-.]+)/$', 'FileHttpResponse', name='file_http_response'),
    url(r'^experiment/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/(?P<filename>[A-Za-z0-9\w.,-]+)$', 'FileHttpResponse', name='file_http_response'),
    
    # login and logout
    url(r'^$', 'LoginView', name='login'),
    url(r'^logout/$', 'LogoutView', name='logout'),

    # upload: can be deleted later
    #url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/$', 'UploadFileView', name='upload'),

    #All upload urls can be deleted later
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitdescription/$', 'EditHitDescriptionView', name='hit_description'),
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitpayment/$', 'EditHitPaymentView', name='hit_payment'),
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/bonuspayment/$', 'EditBonusPaymentView', name='bonus_payment'),
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/hitkeywords/$', 'EditHitKeywordView', name='hit_keyword'),
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/sandbox/$', 'EditSandboxView', name='sandbox'),
    # url(r'^upload/(?P<username>[A-Za-z0-9]+)/(?P<experiment>[A-Za-z0-9,.-]+)/tasknumber/$', 'EditTaskNumberView', name='task_number'),

    #url(r'^userprofile/$', 'UserProfileView', name='user_profile'),
    url(r'^profile/$', 'ProfileGalleryView', name='user_profile'),
    url(r'^viewresults', 'ViewResults', name='ViewResults'),
)
