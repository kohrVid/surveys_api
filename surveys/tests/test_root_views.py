from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class RootViewsTest(TestCase):
    def test_get_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'text/plain')
        self.assertEqual(response.content, b'Surveys API')

    def test_get_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'text/plain')
        self.assertEqual(response.content, b'OK')

    def test_get_health_ignores_trailing_slash(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'text/plain')
        self.assertEqual(response.content, b'OK')
