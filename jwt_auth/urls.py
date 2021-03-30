"""pet_hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from .settings import common
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from schema_graph.views import Schema
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# Admin Site Config
admin.sites.AdminSite.site_header = 'JWT Auth administration'
admin.sites.AdminSite.site_title = 'JWT Auth site admin'
admin.sites.AdminSite.index_title = 'JWT Auth admin dashboard'

urlpatterns1 = static(common.MEDIA_URL, document_root=common.MEDIA_ROOT)
urlpatterns1 += static(common.STATIC_URL, document_root=common.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('apps.authentication.urls')),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("schema/", Schema.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
schema_view = get_schema_view(
    openapi.Info(
        title="JWT Auth APIs",
        default_version="v1",
        description="JWT Auth API",
        contact=openapi.Contact(email=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=None),
        name="schema-redoc",
    ),
    url(r"^docs/", include_docs_urls(title="pet_hotel")),
]