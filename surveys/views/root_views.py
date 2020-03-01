from django.http import HttpResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import serializers


@swagger_auto_schema(
    method='get',
    query_serializer=serializers.Serializer,
    responses = {
        '200' : 'Surveys API',
        '400': 'Bad Request',
    },
    consumes='',
    produces="text/plain",
     security=[],
    operation_id='/',
    operation_description='API endpoint for the root path',
)
@api_view(['GET'])
def get_root(request):
    """
    API endpoint for the root path
    """
    resp = f'Surveys API'

    return HttpResponse(resp, content_type='text/plain')



@swagger_auto_schema(
    method='get',
    query_serializer=serializers.Serializer,
    responses = {
        '200' : 'OK',
        '400': 'Bad Request',
    },
    consumes='',
    # TODO - The documentation currently doesn't return the correct response
    # type. This appears to be a known problem with the drf-yasg library.
    produces="text/plain",
    security=[],
    operation_id='/health',
    operation_description='API endpoint for the healthcheck',
)
@api_view(['GET'])
def get_health(request):
    """
    API endpoint for the healthcheck
    """
    resp = f'OK'

    return HttpResponse(resp, content_type='text/plain')
