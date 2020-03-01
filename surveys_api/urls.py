"""surveys_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    path('admin/', admin.site.urls),
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers, permissions
from surveys.views import root_views

router = routers.DefaultRouter()

slashless_router = routers.DefaultRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    re_path(r'health/?', root_views.get_health),
    re_path('', root_views.get_root),

    path('', include(router.urls)),
    path('', include(slashless_router.urls)),
    path('admin/', admin.site.urls),
]
