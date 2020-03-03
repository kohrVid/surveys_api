from django.shortcuts import render
from rest_framework import viewsets
from surveys.models.survey import Survey
from surveys.serialisers.survey_serialiser import SurveySerialiser
from rest_framework_extensions.mixins import NestedViewSetMixin

class SurveysViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows surveys to be viewed or edited.
    """
    queryset = Survey.objects.all().order_by('-pk')
    serializer_class = SurveySerialiser
