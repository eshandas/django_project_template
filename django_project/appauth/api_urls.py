from django.urls import path

from .api_views import (
    LoginAPI,
    LogoutAPI,
)

app_name = 'appauth_api'
urlpatterns = (
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
)
