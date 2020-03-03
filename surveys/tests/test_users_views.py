import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from surveys.models.survey import Survey
from surveys.models.survey_response import SurveyResponse
from surveys.tests.factories.user_factories import UserFactory
from surveys.tests.factories.survey_factories import SurveyFactory
from surveys.tests.factories.survey_response_factories import SurveyResponseFactory

class UserSurveysViewsTest(TestCase):
    def test_list(self):
        user = UserFactory.create()
        SurveyFactory.create(user_id=user.pk)

        response = self.client.get("/users/{}/surveys".format(user.id))
        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(len(resp_content), 1)

    def test_list_does_not_show_other_user_surveys(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create(pk=2, username="test")
        SurveyFactory.create(user_id=user1.pk)
        SurveyFactory.create(pk=2, user_id=user2.pk)

        response = self.client.get("/users/{}/surveys".format(user1.id))
        resp_content = json.loads(response.content)

        user_ids = list(map(lambda x: x['user_id'], resp_content))

        self.assertIn(user1.id, user_ids )
        self.assertNotIn(user2.id, user_ids)
        self.assertEqual(len(resp_content), 1)

    def test_get(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        response = self.client.get(
                "/users/{}/surveys/{}".format(user.id, survey.id)
        )

        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['id'], survey.id)
        self.assertEqual(resp_content['available_places'], survey.available_places)
        self.assertEqual(resp_content['user_id'], user.id)

    def test_get_does_not_show_other_user_surveys(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create(pk=2, username="test")
        SurveyFactory.create(user_id=user1.pk)
        survey2 = SurveyFactory.create(pk=2, user_id=user2.pk)

        response = self.client.get("/users/{}/surveys{}".format(user1.id, survey2.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post(self):
        user = UserFactory.create()
        data = {
                "name": "Opinions about apples",
                "available_places": 30,
                "user_id": user.id
        }

        self.assertEqual(Survey.objects.count(), 0)
        response = self.client.post("/users/{}/surveys".format(user.id), data=data)
        resp_content = json.loads(response.content)
        self.assertEqual(Survey.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['name'], data['name'])
        self.assertEqual(resp_content['available_places'], data['available_places'])


    def test_put(self):
        client = APIClient()
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        data = {
                "name": "Opinions about oranges",
                "available_places": 30
        }

        response = client.put(
                "/users/{}/surveys/{}/".format(user.id, survey.id),
                data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')


    def test_patch(self):
        client = APIClient()
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        data = {
                "name": "Opinions about oranges"
        }

        response = client.patch(
                "/users/{}/surveys/{}/".format(user.id, survey.id),
                data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')


    def test_delete(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        response = self.client.delete(
                "/users/{}/surveys/{}".format(user.id, survey.id)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class UserSurveysResponseViewsTest(TestCase):
    def test_list(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        response = self.client.get("/users/{}/survey-responses".format(user.id))
        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(len(resp_content), 1)

    def test_list_does_not_show_other_user_surveys(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create(username="test")
        survey = SurveyFactory.create(user_id=user1.pk)

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user1.pk
        )

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user2.pk
        )

        response = self.client.get("/users/{}/survey-responses".format(user1.id))
        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')

        user_ids = list(map(lambda x: x['user_id'], resp_content))

        self.assertIn(user1.pk, user_ids )
        self.assertNotIn(user2.pk, user_ids)
        self.assertEqual(len(resp_content), 1)

    def test_get(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        survey_response = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        response = self.client.get(
                "/users/{}/survey-responses/{}".format(user.id, survey_response.id)
        )

        resp_content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type', ''), 'application/json')
        self.assertEqual(resp_content['id'], survey_response.pk)
        self.assertEqual(resp_content['survey_id'], survey.id)
        self.assertEqual(resp_content['user_id'], user.id)
        self.assertIsNotNone(resp_content['created_at'])

    def test_get_does_not_show_other_user_surveys(self):
        user1 = UserFactory.create()
        user2 = UserFactory.create(username="test")
        survey = SurveyFactory.create(user_id=user1.pk)

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user1.pk
        )

        survey_response2 = SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user2.pk
        )

        response = self.client.get(
                "/users/{}/survey-responses/{}".format(user1.id, survey_response2)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)
        available_places = survey.available_places

        data = {
                "survey_id": survey.id,
                "user_id": user.id
        }

        self.assertEqual(SurveyResponse.objects.count(), 0)

        response = self.client.post(
                "/users/{}/survey-responses".format(user.id),
                data=data
        )

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
        response = self.client.post(
                "/users/{}/survey-responses".format(user.id),
                data=data
        )

        self.assertEqual(SurveyResponse.objects.count(), original_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn(
                'No more available places for this survey',
                response.content.decode("utf-8")
        )


    def test_put(self):
        user = UserFactory.create()
        survey = SurveyFactory.create(user_id=user.pk)

        SurveyResponseFactory.create(
                survey_id=survey.pk,
                user_id=user.pk
        )

        data = {
                "survey_id": 100,
                "user_id": 200
        }

        response = self.client.put(
                "/users/{}/survey-responses/{}".format(user.id,survey.id),
                data=data
        )

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
                "user_id": 200,
        }

        response = self.client.patch(
                "/users/{}/survey-responses/{}".format(user.id, survey_response.id),
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
                "/users/{}/survey-responses/{}".format(user.id, survey_response.id)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
