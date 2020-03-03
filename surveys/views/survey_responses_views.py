from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework_extensions.mixins import NestedViewSetMixin
from surveys.models.survey import Survey
from surveys.models.survey_response import SurveyResponse
from surveys.serialisers.survey_response_serialiser import SurveyResponseSerialiser

class SurveyResponsesViewSet(
        NestedViewSetMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.ReadOnlyModelViewSet
):
    """
    API endpoint that allows survey responses to be viewed or edited.
    """
    queryset = SurveyResponse.objects.all().order_by('-pk')
    serializer_class = SurveyResponseSerialiser

    def create(self, request, *args, **kwargs):
        try:
            survey_response = super().create(request, *args, **kwargs)
            survey = Survey.objects.filter(pk=request.data['survey_id'])
            available_places= survey.first().available_places
            survey.update(available_places = available_places-1)

            return survey_response

        except ValidationError as e:
            return HttpResponse(e.args, status=status.HTTP_400_BAD_REQUEST)
