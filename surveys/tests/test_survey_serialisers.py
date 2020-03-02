from django.test import TestCase
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from surveys.serialisers.survey_serialiser import SurveySerialiser
from surveys.tests.factories.survey_factories import SurveyFactory
from surveys.tests.factories.user_factories import UserFactory

class SurveySerialiserTest(TestCase):
    def test_model_fields(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        user = UserFactory.create()
        survey = SurveyFactory(user_id=user.pk)

        serialiser_context = {
                'request': Request(request),
        }   
        
        for field_name in ['name', 'available_places', 'user_id']:
            self.assertEqual(
                SurveySerialiser(
                    instance=survey,
                    context=serialiser_context
                ).data[field_name],
                getattr(survey, field_name)
            )
