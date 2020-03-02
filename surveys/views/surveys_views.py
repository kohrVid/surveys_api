from django.shortcuts import render
from rest_framework import viewsets
from surveys.models.survey import Survey
from surveys.serialisers.survey_serialiser import SurveySerialiser

class SurveysViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows surveys to be viewed or edited.
    """
    queryset = Survey.objects.all().order_by('-pk')
    serializer_class = SurveySerialiser
