# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns(
    'expdeploy.imageloader.views',
    url(r'^gallery/$', 'gallery', name='gallery'),
)