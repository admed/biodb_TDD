from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                                                        "id":"username_input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                                        "id":"password_input"}))

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
            widget=forms.PasswordInput(attrs={
            "id":"password_input",
            "placeholder": "password"
            })
        )
    confirm_password = forms.CharField(
            widget=forms.PasswordInput(attrs={
            "id":"confirm_input",
            "placeholder": "confirm password"
            })
        )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        users = User.objects.filter(Q(username=username) | Q(email=email))
        if users:
            self.add_error(None,
                              "User with such username or email already exists")
        if password != confirm_password:
            self.add_error(None, "Passwords doesn't match.")
