from django import forms

from .models import (
    AppUser,
)


class AppUserForm(forms.ModelForm):
    email = forms.CharField(disabled=True)

    class Meta:
        model = AppUser
        fields = (
            'email', 'first_name', 'last_name', 'phone_number')
