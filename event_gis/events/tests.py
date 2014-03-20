# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

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

class REST_tests(APITestCase):

    fixtures = ['events.json',]

    def test_fixture(self):
        expected_first_name = u'Stand-up в антикафе Happy People'

        factory = APIRequestFactory()
        request = factory.get('/all_events/')

        view = ListAllEvents.as_view()
        response = view(request)
        response.render() #Here string is rendered for some reason

        import json
        real_first_name = json.loads(response.content)[0].get('name')

        self.assertEqual(real_first_name, expected_first_name)
