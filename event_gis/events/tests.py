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
from events.views import ListAllEvents
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
        self.response = json.loads(response.content)
        self.sorted_events = Event.objects.order_by('name')


    def test_fixture_count(self):
        self.assertEqual(len(self.response), Event.objects.count())  

    #Maybe there is a more pythonic way for next tests

    def test_fixture_ordered_by_name(self):
        for i in xrange( 1, len(self.sorted_events) ):
            self.assertLess(self.response[i-1].get('name'), self.response[i].get('name'))

    def test_fixture_contents(self):
        for i in xrange( 0, len(self.sorted_events) ):
            self.assertEqual(self.response[i].get('name'), self.sorted_events[i].name)
            self.assertEqual(self.response[i].get('location'), self.sorted_events[i].location)
