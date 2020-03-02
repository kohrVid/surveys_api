from django.shortcuts import render
from rest_framework import viewsets
from surveys.models.survey import Survey
from surveys.serialisers.survey_serialiser import SurveySerialiser
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

class SurveysViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Survey.objects.all().order_by('-pk')
    serializer_class = SurveySerialiser
