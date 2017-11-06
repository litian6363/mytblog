#!usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'mytlogin'

urlpatterns = [

    url(r'^signin', views.signin, name='signin'),

    url(r'^signup', views.signup, name='signup'),

    url(r'^save_user', views.save_user, name='save_user'),

    url(r'^check_user', views.check_user, name='check_user'),

    url(r'^complete', views.complete, name='complete'),

    url(r'^logout', views.logout, name='logout'),

]