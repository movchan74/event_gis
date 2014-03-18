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

class REST_tests(APITestCase):
    def test_dummy(self):
        data = ['tratata', 'kekeke', 'alalala']
        response = self.client.get('/rest_dummy/', format='json')
        self.assertEqual(response.data, data_false)