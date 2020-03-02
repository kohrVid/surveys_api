from django import forms
from django.test import TestCase
from surveys.models.survey import Survey

class SurveyTest(TestCase):
    def test_survey_name_is_under_255_characters(self):
        name = "a"*256
        available_places = 4
        survey = Survey.create(name, available_places)
        with self.assertRaises(forms.ValidationError):
            survey.full_clean()
