# coding=utf-8

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from events.views import ListAllEvents, GetEventInfo
from events.models import Event

class REST_tests(APITestCase):

    fixtures = ['events.json',]

    def setUp(self):
        factory = APIRequestFactory()

        request = factory.get('/all_events/')
        view = ListAllEvents.as_view()

        response = view(request)
        response.render() #Here string is rendered for some reason
        import json
        self.all_events_response = json.loads(response.content)
        self.sorted_events = Event.objects.order_by('name')

    #UTILITIES

    def get_event_info_response(self,event_id):
        factory = APIRequestFactory()

        request = factory.get('/event_info/')
        view = GetEventInfo.as_view()

        response = view( request, pk = event_id )
        response.render() #Here string is rendered for some reason

        import json
        return {'content': json.loads(response.content), 'status': response.status_code}


    #TEST: http://127.0.0.1:8000/all_events/

    def test_all_events_count(self):
        self.assertEqual(len(self.all_events_response), Event.objects.count())  

    def test_all_events_ordered_by_name(self):
        for i in xrange( 1, len(self.sorted_events) ):
            self.assertLess(self.all_events_response[i-1].get('name'), self.all_events_response[i].get('name'))

    def test_all_events_contents(self):
        for i in xrange( 0, len(self.sorted_events) ):
            self.assertEqual(self.all_events_response[i].get('id'), self.sorted_events[i].id)
            self.assertEqual(self.all_events_response[i].get('name'), self.sorted_events[i].name)
            self.assertEqual(self.all_events_response[i].get('location'), self.sorted_events[i].location)

    #TEST: http://127.0.0.1:8000/event_info/<id>/

    def test_event_info_contents(self):
        for i in xrange( 1, Event.objects.count() ):
            event_info_response = self.get_event_info_response(i).get('content')
            self.assertEqual(event_info_response.get('id'), Event.objects.get(id=i).id)
            self.assertEqual(event_info_response.get('name'), Event.objects.get(id=i).name)
            self.assertEqual(event_info_response.get('description'), Event.objects.get(id=i).description)
            self.assertEqual(event_info_response.get('address'), Event.objects.get(id=i).address)
            self.assertEqual(event_info_response.get('location'), Event.objects.get(id=i).location)
            self.assertEqual(event_info_response.get('event_type'), Event.objects.get(id=i).event_type)

            import time
            start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime( event_info_response.get('start_time'), "%Y-%m-%dT%H:%M:%SZ" ))
            self.assertEqual( start_time_str  , Event.objects.get(id=i).start_time.strftime("%Y-%m-%d %H:%M:%S"))
            end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime( event_info_response.get('end_time'), "%Y-%m-%dT%H:%M:%SZ" ))
            self.assertEqual( end_time_str  , Event.objects.get(id=i).end_time.strftime("%Y-%m-%d %H:%M:%S"))


    def test_event_info_error_out_of_range(self):
        
        from rest_framework.status import HTTP_404_NOT_FOUND
        self.assertEqual(self.get_event_info_response(0).get('status'), HTTP_404_NOT_FOUND)
        self.assertEqual(self.get_event_info_response(-1).get('status'), HTTP_404_NOT_FOUND)
        self.assertEqual(self.get_event_info_response(Event.objects.count() + 1).get('status'), HTTP_404_NOT_FOUND)

        self.assertEqual(self.get_event_info_response(0).get('content').get('detail'), 'Not found')
        self.assertEqual(self.get_event_info_response(-1).get('content').get('detail'), 'Not found')
        self.assertEqual(self.get_event_info_response( Event.objects.count() + 1 ).get('content').get('detail'), 'Not found')



