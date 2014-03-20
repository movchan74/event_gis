# coding=utf-8
from django.conf.urls import patterns, include, url

from views import render_main_page
from views import ListAllEvents

urlpatterns = patterns('',
    url(r'^$', render_main_page),
    url(r'^all_events/', ListAllEvents.as_view()),
)
