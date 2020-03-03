from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from surveys.views import user_views, surveys_views, survey_responses_views


user_surveys_router = ExtendedSimpleRouter()
user_survey_responses_router = ExtendedSimpleRouter()

user_surveys_router.register(
        r'users',
        user_views.UserViewSet,
        basename='users'
).register(
        r'surveys',
        surveys_views.SurveysViewSet,
        basename='surveys',
        parents_query_lookups=['user_id']
)

user_survey_responses_router.register(
        r'users',
        user_views.UserViewSet,
        basename='users'
).register(
        r'survey-responses',
        survey_responses_views.SurveyResponsesViewSet,
        basename='survey-responses',
        parents_query_lookups=['user_id']
)

slashless_user_surveys_router = routers.DefaultRouter(trailing_slash=False)
slashless_user_surveys_router.registry = user_surveys_router.registry[:]
slashless_user_survey_responses_router = routers.DefaultRouter(trailing_slash=False)
slashless_user_survey_responses_router.registry = user_survey_responses_router.registry[:]
