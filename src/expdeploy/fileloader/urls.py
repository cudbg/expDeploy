from django.conf.urls import patterns, url

urlpatterns = patterns(
    'expdeploy.fileloader.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^list/delete/$', 'delete', name='delete')
    #url(r'^experiment/$', 'uploaded_page', name="uploaded_page")
)
