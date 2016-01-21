# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'expdeploy.planout_test.views',
    url(r'^$', 'planout', name='planout'),
)