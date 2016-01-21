# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'expdeploy.templateloader.views',
    url(r'^$', 'experiment', name='experiment'),
)