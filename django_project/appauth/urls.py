from django.urls import path

from .views import (
    Login,
    Logout,
    ForgotPassword,
    ResetPassword,
    ChangePassword,
    UserInfo,
    Dashboard,
)

app_name = 'appauth'
urlpatterns = (
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password/forgot/', ForgotPassword.as_view(), name='forgot_password'),
    path('password/reset/', ResetPassword.as_view(), name='reset_password'),
    path('password/change/', ChangePassword.as_view(), name='change_password'),
    path('info/', UserInfo.as_view(), name='userinfo'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
)