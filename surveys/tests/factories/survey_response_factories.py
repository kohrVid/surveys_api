from surveys.models.survey_response import SurveyResponse
from factory.django import DjangoModelFactory
from faker import Faker

class SurveyResponseFactory(DjangoModelFactory):
    class Meta:
        model = SurveyResponse
