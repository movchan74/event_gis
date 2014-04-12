# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_main_page(request):
	default_lon = '37.6461231656120958'
	default_lat = '55.7572258153171276'
	return render_to_response('main_page.html', {'lon' : default_lon, 'lat' : default_lat}, context_instance=RequestContext(request))



from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import UnicodeJSONRenderer
from events.models import Event, EventType
from events.serializers import EventSerializer, EventTypeSerializer
from datetime import datetime

# http://127.0.0.1:8000/filter_events?type=1+2+3&start_time=2000-1-25+13-30&end_time=2015-10-26+13-30
class FilterEvents(ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventSerializer

    def get_queryset(self):
        query_objects = Event.objects.all()

        if 'type' in self.request.QUERY_PARAMS:
            types = self.request.QUERY_PARAMS.get('type').split()
            types = map( int, types )
            query_objects = query_objects.filter( event_type__in = types )

        if 'start_time' in self.request.QUERY_PARAMS:
            start_time_str = self.request.QUERY_PARAMS.get('start_time')
            start_time = datetime.strptime( start_time_str, "%Y-%m-%d %H-%M" )
            query_objects = query_objects.filter( start_time__gt = start_time )

        if 'end_time' in self.request.QUERY_PARAMS:
            end_time_str = self.request.QUERY_PARAMS.get('end_time')
            end_time = datetime.strptime( end_time_str, "%Y-%m-%d %H-%M" )
            query_objects = query_objects.filter( end_time__lt = end_time )

        return query_objects.order_by('id')


# http://127.0.0.1:8000/event_types
class EventTypes(ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventTypeSerializer

    def get_queryset(self):
        return EventType.objects.all()



