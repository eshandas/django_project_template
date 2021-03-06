"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf import settings

from .views import IndexView, health
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='{{ project_name }} APIs')

v1 = settings.VERSION['v1']

admin.site.site_header = '{{ project_name }}'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('api/', schema_view, name='swagger'),
    path('health/', health, name='health'),

    # --- Appauth
    path('auth/', include('appauth.urls')),
    path('api/%s/auth/' % v1, include('appauth.api_urls')),

    # --- Posts
    path('posts/', include('posts.urls')),
    path('api/%s/posts/' % v1, include('posts.api_urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
