from django.conf.urls import patterns, url
from .views import UploadView

urlpatterns = patterns(
    'expdeploy.testapp.views',
    url(r'^$', 'UploadView', name='uploaaaaaaaad'),
    #no success view added
)
#url(r'^snippets/$', snippets.views.SnippetListView.as_view()),