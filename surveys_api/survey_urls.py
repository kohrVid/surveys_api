from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from surveys.views import surveys_views, survey_responses_views


survey_responses_router = ExtendedSimpleRouter()

survey_responses_router.register(
        r'surveys',
        surveys_views.SurveysViewSet,
        basename='surveys'
).register(
        r'survey-responses',
        survey_responses_views.SurveyResponsesViewSet,
        basename='survey-responses',
        parents_query_lookups=['survey_id']
)

slashless_survey_responses_router = routers.DefaultRouter(trailing_slash=False)
slashless_survey_responses_router.registry = survey_responses_router.registry[:]
