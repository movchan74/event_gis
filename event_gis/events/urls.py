from django.conf.urls import patterns, include, url

from views import render_main_page

urlpatterns = patterns('',
	url(r'^$', render_main_page),
)
