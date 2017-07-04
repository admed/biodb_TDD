from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
class SignUpForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(attrs={
                "id":"username_input",
                "placeholder": "username"
            })
        )
    email = forms.CharField(
            widget=forms.TextInput(attrs={
            "id":"email_input",
            "placeholder": "email"
            })
        )
    password = forms.CharField(
            widget=forms.TextInput(attrs={
            "id":"password_input",
            "placeholder": "password"
            })
        )
    confirm_password = forms.CharField(
            widget=forms.TextInput(attrs={
            "id":"confirm_input",
            "placeholder": "confirm password"
            })
        )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        message = "User with such username or email already exists"
        try:
            User.objects.get(username=username)
            raise ValidationError(_(message))
        except User.DoesNotExist:
            pass
        try:
            User.objects.get(email=email)
            raise ValidationError(_(message))
        except User.DoesNotExist:
            pass
