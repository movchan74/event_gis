# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_main_page(request):
	default_lon = '37.6461231656120958'
	default_lat = '55.7572258153171276'
	return render_to_response('main_page.html', {'lon' : default_lon, 'lat' : default_lat}, context_instance=RequestContext(request))



from rest_framework import generics
from rest_framework.renderers import UnicodeJSONRenderer
from events.models import Event
from events.serializers import EventSerializer

# http://127.0.0.1:8000/all_events/
class ListAllEvents(generics.ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.order_by('name')
