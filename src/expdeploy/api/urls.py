from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^ban', views.ban, name='ban'),
	url(r'^payoutAll', views.payout, name='payoutAll'),
	url(r'^payout', views.payout, name='payout'),
	url(r'^results', views.results, name='results'),
	url(r'^removemturk', views.removemturk, name='removemturk'),
	url(r'^mturk', views.mturk, name='mturk'),
	url(r'^result', views.result, name='result'),
	url(r'^task', views.task, name='task'),
	url(r'^finishTasks', views.finishTasks, name='end'),
	url(r'^experiment', views.experiment, name='experiment'),
	url(r'^log/', views.log, name='log'),
	url(r'^export', views.export, name='export'),
    url(r'^$', views.index, name='index'),
]