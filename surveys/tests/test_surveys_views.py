import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from surveys.models.survey import Survey
from surveys.tests.factories.user_factories import UserFactory

class SurveysViewsTest(TestCase):
    def test_post(self):
        user = UserFactory.create()
        data = {
                "name": "Opinions about apples",
                "available_places": 30,
                "user_id": user.id
        }

        self.assertEqual(Survey.objects.count(), 0)
        response = self.client.post("/surveys", data=data)
        resp_content = json.loads(response.content)
        self.assertEqual(Survey.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['name'], data['name'])
        self.assertEqual(resp_content['available_places'], data['available_places'])
        self.assertEqual(resp_content['user_id'], user.id)
