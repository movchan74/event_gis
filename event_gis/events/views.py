# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_main_page(request):
	default_lon = '37.6461231656120958'
	default_lat = '55.7572258153171276'
	return render_to_response('main_page.html', {'lon' : default_lon, 'lat' : default_lat}, context_instance=RequestContext(request))



from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import UnicodeJSONRenderer
from events.models import Event
from events.serializers import EventSerializer
from datetime import datetime

# http://127.0.0.1:8000/filter_events?type=1+3&start_time=2013-10-25+13-30&end_time=2013-10-26+10-00
class FilterEvents(ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventSerializer

    def get_queryset(self):
        types = self.request.QUERY_PARAMS.get('type').split()
        types = map( int, types )

        start_time_str = self.request.QUERY_PARAMS.get('start_time')
        start_time = datetime.strptime( start_time_str, "%Y-%m-%d %H-%M" )

        end_time_str = self.request.QUERY_PARAMS.get('end_time')
        end_time = datetime.strptime( end_time_str, "%Y-%m-%d %H-%M" )

        return Event.objects.filter( event_type__in = types ).filter( start_time__gt = start_time).filter( end_time__lt = end_time )

