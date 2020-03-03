from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from surveys.models.survey_response import SurveyResponse
from surveys.serialisers.survey_response_serialiser import SurveyResponseSerialiser

class SurveyResponsesViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.ReadOnlyModelViewSet
):
    """
    API endpoint that allows survey responses to be viewed or edited.
    """
    queryset = SurveyResponse.objects.all().order_by('-pk')
    serializer_class = SurveyResponseSerialiser

