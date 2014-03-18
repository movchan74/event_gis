from django.conf.urls import patterns, include, url

from views import render_main_page
from views import REST_DummyView

urlpatterns = patterns('',
	url(r'^$', render_main_page),
    url(r'^rest_dummy/', REST_DummyView.as_view()),
)
