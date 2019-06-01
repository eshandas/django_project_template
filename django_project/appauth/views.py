from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404

from appauth.mixins import AdminOrOwnerPermission

from django.conf import settings

from appauth.mixins import LoginRequired

from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout

from .models import AppUser

from .forms import AppUserForm

from utils import response_handler

from .decorators import logged_in_access

from .constants import (
    RequestKeys,
    SuccessMessages,
    FailMessages,
)

from global_tasks.email_tasks.emailer import Emailer


class Login(View):
    template_name = 'appauth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('appauth:dashboard'))
        else:
            return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST.get(RequestKeys.EMAIL, None)
        password = request.POST.get(RequestKeys.PASSWORD, None)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session.save()
                    next_page = request.GET.get(RequestKeys.NEXT, None)
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect(reverse('appauth:dashboard'))
                else:
                    return render(
                        request,
                        self.template_name,
                        response_handler.failed_response(FailMessages.USER_INACTIVE))
            else:
                return render(
                    request,
                    self.template_name,
                    response_handler.failed_response(FailMessages.INVALID_CREDENTIALS))
        else:
            return render(
                request,
                self.template_name,
                response_handler.failed_response(FailMessages.INVALID_CREDENTIALS))


class Logout(LoginRequired, View):
    template_name = 'appauth/logout.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('appauth:login'))


class CheckPassword(View):
    template_name = ''

    def get(self, request):
        email = request.GET.get(RequestKeys.EMAIL, None)
        if email:
            try:
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist:
                return Http404
            if user.password == '':
                # User hasn't created a password yet
                if user.password_reset_token == '':
                    user.create_password_reset_token()
                    user.save()
                return HttpResponseRedirect(reverse('appauth:reset_password'))


class ForgotPassword(View):
    template_name = 'appauth/forgot_password.html'

    def _email_token(self, user):
        context = {
            'name': user.name,
            'url': '%s%s?email=%s&token=%s' % (
                settings.SITE_URL,
                reverse('appauth:reset_password'),
                user.email,
                user.password_reset_token)}
        Emailer(
            subject='Change password',
            message='Please set a password so that you can access the dashboard.',
            recipient_list=[user.email],
            email_template='appauth/email_templates/forgot_password.html',
            context=context).send_email(send_async=True, fail_silently=True)

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST.get(RequestKeys.EMAIL, None)
        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return render(
                request,
                self.template_name,
                response_handler.failed_response(FailMessages.INVALID_EMAIL))
        user.create_password_reset_token(save=True)
        self._email_token(user)
        return render(
            request,
            self.template_name,
            response_handler.success_response(SuccessMessages.PASSWORD_RESET))


class ResetPassword(View):
    template_name = 'appauth/reset_password.html'

    def _check_token(self, email, token):
        try:
            user = AppUser.objects.get(
                email=email,
                password_reset_token=token)
            return user
        except AppUser.DoesNotExist:
            raise Http404

    def get(self, request):
        email = request.GET.get(RequestKeys.EMAIL, None)
        token = request.GET.get(RequestKeys.TOKEN, None)

        if email and token:
            user = self._check_token(email, token)
            context = {
                RequestKeys.EMAIL: email,
                RequestKeys.TOKEN: token}
            if user:
                return render(request, self.template_name, context)
        else:
            raise Http404

    def post(self, request):
        email = request.GET.get(RequestKeys.EMAIL, None)
        token = request.GET.get(RequestKeys.TOKEN, None)
        password = request.POST.get(RequestKeys.PASSWORD, None)
        confirm_password = request.POST.get(RequestKeys.CONFIRM_PASSWORD, None)

        if password != confirm_password or len(password) < 8:
            context = {
                RequestKeys.EMAIL: email,
                RequestKeys.TOKEN: token}
            context.update(response_handler.failed_response(FailMessages.INVALID_PASSWORD))
            return render(
                request,
                self.template_name,
                context)

        if email and token:
            user = self._check_token(email, token)
            if user:
                user.password_reset_token = ''
                user.set_password(password)
                user.save()
                return HttpResponseRedirect(reverse('appauth:login'))
        else:
            raise Http404


class ChangePassword(View):
    template_name = 'appauth/change_password.html'

    def _email_notification(self, user):
        context = {
            'name': user.name}
        Emailer(
            subject='Password changed successfully',
            message='Your password has been changed successfully.',
            recipient_list=[user.email],
            email_template='appauth/email_templates/change_password.html',
            context=context).send_email(send_async=True, fail_silently=True)

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        password = request.POST.get(RequestKeys.PASSWORD, None)
        confirm_password = request.POST.get(RequestKeys.CONFIRM_PASSWORD, None)

        if password != confirm_password or len(password) < 8:
            return render(
                request,
                self.template_name,
                response_handler.generic_response(FailMessages.INVALID_PASSWORD))

        request.user.set_password(password)
        request.user.save()
        self._email_notification(request.user)
        logout(request)
        return HttpResponseRedirect(reverse('appauth:login'))


class UserInfo(LoginRequired, View):
    template_name = 'appauth/user_info.html'

    @method_decorator(logged_in_access)
    def get(self, request):
        context = {
            'form': AppUserForm(instance=request.user)}
        return render(request, self.template_name, context)

    @method_decorator(logged_in_access)
    def post(self, request):
        form = AppUserForm(request.POST, instance=request.user)
        context = {}
        if form.is_valid():
            form.save()
            context = response_handler.alert_response(
                response_handler.SUCCESS,
                'Information was saved successfully.',
                'Success!')
        context['form'] = form
        return render(request, self.template_name, context)


class Dashboard(LoginRequired, View):
    template_name = 'appauth/dashboard.html'

    @method_decorator(logged_in_access)
    def get(self, request):
        return render(request, self.template_name, {})
