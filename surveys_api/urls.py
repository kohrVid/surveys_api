from decouple import config
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions
from surveys.views import root_views, user_views, surveys_views, survey_responses_views
from .survey_urls import survey_responses_router, slashless_survey_responses_router
from .user_urls import user_surveys_router, slashless_user_surveys_router, user_survey_responses_router, slashless_user_survey_responses_router

router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'groups', user_views.GroupViewSet)
router.register(r'surveys', surveys_views.SurveysViewSet)
router.register(
        r'survey-responses',
        survey_responses_views.SurveyResponsesViewSet
)

slashless_router = routers.DefaultRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

schema_view = get_schema_view(
        openapi.Info(
          title=config('APP_TITLE'),
          default_version=config('VERSION'),
          description=config('DESCRIPTION'),
          terms_of_service=config('TERMS_OF_SERVICE'),
          contact=openapi.Contact(email=config('AUTHOR_EMAIL')),
          license=openapi.License(name=config('LICENCE')),
       ),
       public=True,
       permission_classes=(
           permissions.AllowAny,
       ),
)

urlpatterns = [
    re_path(r'health/?', root_views.get_health),

    re_path(
        '^swagger-ui/?',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),

    re_path(
        '^swagger(?P<format>.json|.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', root_views.get_root),
    path('', include(router.urls)),
    path('', include(user_surveys_router.urls)),
    path('', include(user_survey_responses_router.urls)),
    path('', include(survey_responses_router.urls)),

    path('', include(slashless_router.urls)),
    path('', include(slashless_survey_responses_router.urls)),
    path('', include(slashless_user_surveys_router.urls)),
    path('', include(slashless_user_survey_responses_router.urls)),
]
