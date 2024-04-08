"""market_stocks_price URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib.auth.decorators import permission_required

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator

from rest_framework import permissions


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Market Products API",
        default_version="v1",
        description="Api for products check on the market",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name=""),
    ),
    public=settings.SWAGGER_PUBLIC,
    generator_class=CustomSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "",
        permission_required('IsAdminUser', login_url="/admin/login/?next=/")
        (schema_view.with_ui("swagger", cache_timeout=0)),
        name="schema-swagger-ui"
    ),

    path('admin/', admin.site.urls),

    path('api/products/', include('products.urls')),
]
