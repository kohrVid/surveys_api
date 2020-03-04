import json

from django.test import TestCase
from rest_framework import status
from surveys.models.survey import Survey
from surveys.models.survey_response import SurveyResponse
from surveys.tests.factories.user_factories import UserFactory
from surveys.tests.factories.survey_factories import SurveyFactory
from surveys.tests.factories.survey_response_factories import SurveyResponseFactory

class SurveyResponsesViewsTest(TestCase):
    def test_list(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        response = self.client.get("/survey-responses")
        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(len(resp_content), 1)


    def test_get(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        survey_response = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        response = self.client.get("/survey-responses/{}".format(survey_response.pk))
        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['id'], survey_response.pk)
        self.assertEqual(resp_content['survey_id'], survey.id)
        self.assertEqual(resp_content['user_id'], user.id)
        self.assertIsNotNone(resp_content['created_at'])


    def test_post(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)
        available_places = survey.available_places

        data = {
                "survey_id": survey.id,
                "user_id": user.id
        }

        self.assertEqual(SurveyResponse.objects.count(), 0)
        response = self.client.post("/survey-responses", data=data)
        resp_content = json.loads(response.content)
        self.assertEqual(SurveyResponse.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['survey_id'], survey.id)
        self.assertEqual(resp_content['user_id'], user.id)
        self.assertIsNotNone(resp_content['created_at'])

        self.assertEqual(
                Survey.objects.get(pk=survey.pk).available_places,
                available_places-1
        )


    def test_post_if_unavailable(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(available_places=0, user_id=user.pk)

        data = {
                "survey_id": survey.id,
                "user_id": user.id
        }

        original_count = SurveyResponse.objects.count()
        response = self.client.post("/survey-responses", data=data)

        self.assertEqual(SurveyResponse.objects.count(), original_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn(
                'No more available places for this survey',
                response.content.decode("utf-8")
        )


    def test_put(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        survey_response = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        data = {
                "survey_id": 100,
                "user_id": 200
        }

        response = self.client.put("/survey-responses/{}".format(survey_response.pk), data=data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')


    def test_patch(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        survey_response = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        data = {
                "survey_id": 100,
        }

        response = self.client.patch(
                "/survey-responses/{}".format(survey_response.pk),
                data=data
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')


    def test_delete(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        survey_response = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        response = self.client.delete(
                "/survey-responses/{}".format(survey_response.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
