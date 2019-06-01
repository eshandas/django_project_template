from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from appauth.models import AppUser


class Permission(object):
    def not_logged_in(self, next=None):
        if next:
            return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + next)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)


class LoginRequired(Permission):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(LoginRequired, self).dispatch(request, *args, **kwargs)
        else:
            return self.not_logged_in(
                next=request.get_full_path())


class AdminPermission(Permission):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return super(AdminPermission, self).dispatch(request, *args, **kwargs)
        elif request.user.is_anonymous():
            return self.not_logged_in(
                next=request.get_full_path())


class AdminOrOwnerPermission(Permission):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return self.not_logged_in(
                next=request.get_full_path())
        elif request.user.is_authenticated and not request.user.is_admin:
            return super(AdminOrOwnerPermission, self).dispatch(request, *args, **kwargs)
        elif request.user.is_admin:
            mock_user = request.session.get('mock_user', None)
            if mock_user:
                request.user = AppUser.objects.get(email=mock_user)
                return super(AdminOrOwnerPermission, self).dispatch(request, *args, **kwargs)
            else:
                return self.go_to_admin()

    def go_to_admin(self):
        return HttpResponseRedirect(reverse('admin:index'))
