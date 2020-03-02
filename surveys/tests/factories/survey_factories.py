from surveys.models.survey import Survey
from django_factory import factory
from faker import Faker

class SurveyFactory(factory.Factory):
    pk = 1
    name = Faker().name()
    available_places = 4

    class Meta: 
        model = Survey
