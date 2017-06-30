from django.shortcuts import render
from django.views.generic import View, FormView
from accounts.forms import SignUpForm

# Create your views here.

class LoginView(View):
    def get(self, request, **kwargs):
        return render(request, "accounts/login.html")

class SignUpView(FormView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm
