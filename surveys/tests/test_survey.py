from django import forms
from django.test import TestCase
from surveys.models.survey import Survey, User
from surveys.tests.factories.user_factories import UserFactory

class SurveyTest(TestCase):
    def test_survey_name_is_under_255_characters(self):
        name = "a"*256
        available_places = 4
        user = UserFactory.create()

        survey = Survey.create(name, available_places, user.id)
        with self.assertRaises(forms.ValidationError):
            survey.full_clean()
