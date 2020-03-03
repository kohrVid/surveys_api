from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
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

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return HttpResponse(e.args, status=status.HTTP_400_BAD_REQUEST)
