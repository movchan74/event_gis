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
from events.views import FilterEvents
from events.models import Event

class REST_tests(APITestCase):

    fixtures = ['events.json',]

    # def setUp(self):
        # factory = APIRequestFactory()

        # request = factory.get('/all_events/')
        # view = ListAllEvents.as_view()

        # response = view(request)
        # response.render() #Here string is rendered for some reason
        # import json
        # self.all_events_response = json.loads(response.content)
        # self.sorted_events = Event.objects.order_by('name')

    #UTILITIES

    # def get_event_info_response(self,event_id):
    #     factory = APIRequestFactory()

    #     request = factory.get('/event_info/')
    #     view = GetEventInfo.as_view()

    #     response = view( request, pk = event_id )
    #     response.render() #Here string is rendered for some reason

    #     import json
    #     return {'content': json.loads(response.content), 'status': response.status_code}
    # http://127.0.0.1:8000/filter_events?type=1+2+3&start_time=2000-1-25+13-30&end_time=2015-10-26+13-30







