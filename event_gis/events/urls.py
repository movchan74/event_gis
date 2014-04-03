# coding=utf-8
from django.conf.urls import patterns, include, url

from views import render_main_page
from views import ListAllEvents, GetEventInfo

urlpatterns = patterns('',
    url(r'^$', render_main_page),
    url(r'^all_events$', ListAllEvents.as_view()),
    url(r'^event_info/(?P<pk>[0-9]+)/$', GetEventInfo.as_view()),
)
