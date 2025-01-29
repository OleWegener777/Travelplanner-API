"""
URL configuration for travelplanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static 

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title = "You API for finding the best destinations and travelplans for south east asia!",
        default_version = "v1",
        description ="Find and create travelplans.",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
   permission_classes=(permissions.AllowAny,),
    )


urlpatterns = [
    path("swagger/",schema_view.with_ui("swagger",cache_timeout=0),name="swagger-doc"),
    path("redoc/",schema_view.with_ui("redoc",cache_timeout=0),name="redoc-doc"),
    path("admin/", admin.site.urls),
    path("api/v1/",include("api_app.urls"))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
