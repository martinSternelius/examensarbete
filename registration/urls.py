# -*- coding: utf-8 -*- 
'''
Created on 16 sep 2013

@author: Martin
'''
from django.conf.urls import patterns, url
from registration import views

urlpatterns = patterns('',
    url(r'^$', views.register, name='register'),
)


