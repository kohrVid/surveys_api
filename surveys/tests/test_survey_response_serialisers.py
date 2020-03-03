import datetime

from django.test import TestCase
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from surveys.models.survey_response import SurveyResponse
from surveys.serialisers.survey_response_serialiser import SurveyResponseSerialiser
from surveys.tests.factories.user_factories import UserFactory
from surveys.tests.factories.survey_factories import SurveyFactory
from surveys.tests.factories.survey_response_factories import SurveyResponseFactory

class SurveyResponseSerialiserTest(TestCase):
    def test_model_fields(self):
        factory = APIRequestFactory()
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)
        request = factory.get("/survey-responses/{}".format(1))
        survey_response_factory = SurveyResponseFactory(survey_id=survey.pk, user_id=user.pk)

        serialiser_context = {
                'request': Request(request),
        }

        survey_response_serialiser = SurveyResponseSerialiser(
                instance=survey_response_factory,
                context=serialiser_context
        ).data

        self.assertEqual(
                survey_response_serialiser['survey_id'],
                survey_response_factory.survey_id
        )

        self.assertEqual(
                survey_response_serialiser['user_id'],
                survey_response_factory.user_id
        )
        self.assertIn(
                survey_response_factory.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                survey_response_serialiser['created_at'],
        )

    def test_create(self):
        factory = APIRequestFactory()
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        self.assertEqual(SurveyResponse.objects.count(), 0)

        request = factory.post("/survey-responses/")

        survey_response_factory = SurveyResponseFactory(
                user_id=user.pk,
                survey_id=survey.pk
        )

        serialiser_context = {
                'request': Request(request),
        }

        SurveyResponseSerialiser(
            instance=survey_response_factory,
            context=serialiser_context
        )

        survey_response = SurveyResponse.objects.all().last()

        self.assertEqual(SurveyResponse.objects.count(), 1)
        self.assertEqual(survey_response.survey, survey)
        self.assertEqual(survey_response.user, user)

    def test_create_if_unavailable(self):
        factory = APIRequestFactory()
        user = UserFactory.create()
        survey = SurveyFactory.create(available_places=0, user_id=user.pk)

        survey_response_factory = SurveyResponseFactory(
                user_id=user.pk,
                survey_id=survey.pk
        )

        original_count = SurveyResponse.objects.count()

        request = factory.post("/survey-responses/")

        serialiser_context = {
                'request': Request(request),
        }

        SurveyResponseSerialiser(
            instance=survey_response_factory,
            context=serialiser_context
        )

        self.assertEqual(SurveyResponse.objects.count(), original_count)
