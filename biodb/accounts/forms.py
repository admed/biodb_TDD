from django import forms
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
