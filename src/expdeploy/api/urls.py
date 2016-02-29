from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^mturk', views.mturk, name='mturk'),
	url(r'^result', views.result, name='result'),
	url(r'^task', views.task, name='task'),
	url(r'^experiment', views.experiment, name='experiment'),
	url(r'^log/', views.log, name='log'),
    url(r'^$', views.index, name='index'),
]