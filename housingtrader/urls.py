# -*- coding: utf-8 -*- 
'''
Created on 16 sep 2013

@author: Martin
'''
from django.conf.urls import patterns, url
from housingtrader import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)


