# -*- coding: utf-8 -*- 
'''
Created on 16 sep 2013

@author: Martin
'''
from django.conf.urls import patterns, url
from housingtrader import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^dashboard/', views.index, name='index'),
    url(r'^create_listing/', views.create_listing, name='create_listing'),
    url(r'^(?P<listing_id>\d+)/change_published_state/', views.change_published_state, name='change_published_state'),
    url(r'^(?P<listing_id>\d+)/edit', views.edit_listing, name='edit_listing'),
    url(r'^(?P<pk>\d+)/delete', views.ListingDelete.as_view(), name='delete_listing'),
    url(r'^(?P<listing_id>\d+)/find_trades', views.find_trades, name='find_trades'),
    url(r'^(?P<listing_id>\d+)/(?P<other_listing_id>\d+)/detail', views.detail, name='detail'),
    url(r'^(?P<listing_id>\d+)/(?P<other_listing_id>\d+)/send_trade_request', views.send_trade_request, name='send_trade_request'),
    url(r'^(?P<requester_id>\d+)/(?P<receiver_id>\d+)/trade_request_detail', views.trade_request_detail, name='trade_request_detail'),
    url(r'^(?P<requester_id>\d+)/(?P<receiver_id>\d+)/trade_request_decline', views.trade_request_decline, name='trade_request_decline'),
    url(r'^(?P<listing_id>\d+)/preview', views.preview, name='preview'),
    url(r'^(?P<listing_id>\d+)/public_detail', views.public_detail, name='public_detail'),
)


