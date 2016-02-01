from django.conf.urls import url

from . import views

urlpatterns = [
	
	url(r'^log', views.log, name='log'),
    url(r'^$', views.index, name='index'),
]