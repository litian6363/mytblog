#!usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'polls'

# 设置app的url，由  mysite\urls.py  call过来
urlpatterns = [

    # ex: /polls/
    url(r'^$', views.index, name='index'),

    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote')

]
