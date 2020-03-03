from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from surveys.views import root_views, user_views, surveys_views, survey_responses_views


surveys_router = ExtendedSimpleRouter()
survey_responses_router = ExtendedSimpleRouter()

surveys_router.register(
        r'users',
        user_views.UserViewSet,
        basename='users'
).register(
        r'surveys',
        surveys_views.SurveysViewSet,
        basename='surveys',
        parents_query_lookups=['user_id']
)

survey_responses_router.register(
        r'users',
        user_views.UserViewSet,
        basename='users'
).register(
        r'survey-responses',
        survey_responses_views.SurveyResponsesViewSet,
        basename='survey-responses',
        parents_query_lookups=['user_id']
)

slashless_surveys_router = routers.DefaultRouter(trailing_slash=False)
slashless_surveys_router.registry = surveys_router.registry[:]
slashless_survey_responses_router = routers.DefaultRouter(trailing_slash=False)
slashless_survey_responses_router.registry = survey_responses_router.registry[:]
