from django.contrib.auth.models import User
from surveys.models.survey import Survey
from factory.django import DjangoModelFactory
from faker import Faker

class SurveyFactory(DjangoModelFactory):
    pk = 1
    name = Faker().name()
    available_places = 4

    class Meta: 
        model = Survey
