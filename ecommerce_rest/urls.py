from django.contrib import admin
from django.urls import path, include

# Swagger imports
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import Login, Logout

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de API",
      default_version='v0.1',
      description="Documentacion publica de API Ecommerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alonsotaverna@outlook.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/',include('apps.users.api.urls')),
    path('products/',include('apps.products.api.routers')), # enlazamos al router
    path('', Login.as_view(), name='Login'),
    path('logout/', Logout.as_view(), name='Logout'),
    # Swagger routes
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
