from django.test import TestCase
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from surveys.models.survey import Survey
from surveys.serialisers.survey_serialiser import SurveySerialiser
from surveys.tests.factories.survey_factories import SurveyFactory
from surveys.tests.factories.user_factories import UserFactory

class SurveySerialiserTest(TestCase):
    def test_model_fields(self):
        factory = APIRequestFactory()
        user = UserFactory.create()
        request = factory.get("/surveys/{}".format(1))
        survey_factory = SurveyFactory(user_id=user.pk)

        serialiser_context = {
                'request': Request(request),
        }

        for field_name in ['name', 'available_places', 'user_id']:
            self.assertEqual(
                SurveySerialiser(
                    instance=survey_factory,
                    context=serialiser_context
                ).data[field_name],
                getattr(survey_factory, field_name)
            )

    def test_create(self):
        factory = APIRequestFactory()
        user = UserFactory.create()
        request = factory.post("/surveys/")
        survey_factory = SurveyFactory(user_id=user.pk)

        serialiser_context = {
                'request': Request(request),
        }

        SurveySerialiser(
            instance=survey_factory,
            context=serialiser_context
        )

        survey = Survey.objects.all().last()

        self.assertEqual(survey.name, survey_factory.name)
        self.assertEqual(survey.available_places, survey_factory.available_places)
        self.assertEqual(survey.user, user)
