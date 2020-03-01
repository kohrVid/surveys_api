from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

def get_root(request):
    """
    API endpoint for the root path
    """
    resp = f'Surveys API'

    return HttpResponse(resp, content_type='text/plain')

def get_health(request):
    """
    API endpoint for the healthcheck
    """
    resp = f'OK'

    return HttpResponse(resp, content_type='text/plain')
