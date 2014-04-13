# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import urllib2, json

def render_main_page(request):
	default_lon = '37.6461231656120958'
	default_lat = '55.7572258153171276'
	return render_to_response('main_page.html', {'lon' : default_lon, 'lat' : default_lat}, context_instance=RequestContext(request))

from rest_framework.generics import ListAPIView
from rest_framework.renderers import UnicodeJSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
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
            start_time = datetime.strptime( start_time_str, "%d.%m.%Y %H:%M" )
            query_objects = query_objects.filter( start_time__gt = start_time ) # to do

        if 'end_time' in self.request.QUERY_PARAMS:
            end_time_str = self.request.QUERY_PARAMS.get('end_time')
            end_time = datetime.strptime( end_time_str, "%d.%m.%Y %H:%M" )
            query_objects = query_objects.filter( end_time__lt = end_time )

        return query_objects.order_by('id')

# http://127.0.0.1:8000/make_route?event_ids=1+5+3+2
class MakeRoute(APIView):

    def get_events(self, ids):
        events = Event.objects.filter(id__in = ids).order_by( 'start_time' )
        return events

    def hasTimeIntersections(self, eventTimes):
        for i in xrange(0, len(eventTimes) - 1):
            if eventTimes[i].get("end_time") > eventTimes[i+1].get("start_time"):
                return {"hasTimeIntersections" : True, "first" : eventTimes[i].get("id"), "second" : eventTimes[i+1].get("id") }
        print "No intersections"
        return  {"hasTimeIntersections" : False}

    def getRoute(self, events):
        events = list(events)
        url = 'http://maps.googleapis.com/maps/api/directions/json?'
        start_event = events[0]
        end_event = events[-1]
        waypoints = []
        params = {
            'origin' : '%s,%s' % (start_event.location.y, start_event.location.x),
            'destination' : '%s,%s' % (end_event.location.y, end_event.location.x),
            'sensor' : 'false',
            'language' : 'ru',
        }
        for i in range(1, len(events)-1):
            event = events[i]
            waypoints.append('%s,%s' % (event.location.y, event.location.x))
        params['waypoints'] = '|'.join(waypoints)
        print url + '&'.join([key+'='+params[key] for key in params])
        response = urllib2.urlopen(url + '&'.join([key+'='+params[key] for key in params])).read()
        route = json.loads(response)
        output = {'legs' : []}
        for leg in route['routes'][0]['legs']:
            leg_info = {}
            leg_info['duration'] = leg['duration']['value']
            leg_info['steps'] = []
            for step in leg['steps']:
                step_info = {}
                step_info['text'] = step['html_instructions']
                step_info['polyline'] = step['polyline']['points']
                leg_info['steps'].append(step_info)
            output['legs'].append(leg_info)
        return json.dumps(output)


    def get(self, request, format = None):
        event_ids_string = request.QUERY_PARAMS.get('event_ids').split()
        event_ids = []
        for event in event_ids_string:
            event_ids.append( int(event) )

        events = self.get_events( event_ids )

        eventTimes = [];
        for event in events:
            eventTimes.append(  {"id" : event.id, "start_time" : event.start_time, "end_time" : event.end_time} )

        timeIntersections = self.hasTimeIntersections( eventTimes )

        if ( timeIntersections.get("hasTimeIntersections") ):
            return Response( timeIntersections )
        else:
            route = self.getRoute( events )
            return Response( route )



# http://127.0.0.1:8000/event_types
class EventTypes(ListAPIView):
    renderer_classes = (UnicodeJSONRenderer,)
    serializer_class = EventTypeSerializer

    def get_queryset(self):
        return EventType.objects.all()



