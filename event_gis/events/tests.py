# coding=utf-8

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from events.views import FilterEvents
import time
# from events.models import Event

class REST_tests(APITestCase):

    fixtures = ['events.json',]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FilterEvents.as_view()

    def render_filter_events_response(self, filters):
        request = self.factory.get( '/filter_events', filters, format='json' )
        response = self.view(request)
        response.render() #Here string is rendered for some reason
        import json
        return json.loads(response.content)

    def test_type_filter( self ):
        filters = {'type': '2'}
        filter_events_response = self.render_filter_events_response( filters )
        for event in filter_events_response:
            self.assertEqual( event.get('event_type'), 2 )
        #ToDo incorrect test

    def test_time_filter( self ):
        filters = {'start_time': '25.01.2000 13:30'}
        filters_time = time.strptime( filters.get('start_time'), "%d.%m.%Y %H:%M")

        filter_events_response = self.render_filter_events_response( filters )
        for event in filter_events_response:
            event_time = time.strptime( event.get('start_time'), "%Y-%m-%dT%H:%M:%SZ")
            self.assertLess( filters_time, event_time )







