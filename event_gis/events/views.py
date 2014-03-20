# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import Map

def render_main_page(request):
	m = Map()
	return render_to_response('main_page.html', {'map_form' : m}, context_instance=RequestContext(request))



from rest_framework import generics
from rest_framework.renderers import UnicodeJSONRenderer
from events.models import Event
from events.serializers import EventSerializer

class ListAllEvents(generics.ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.order_by('name')
