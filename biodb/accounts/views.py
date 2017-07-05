from django.shortcuts import render
from django.views.generic import View, FormView
from accounts.forms import SignUpForm
from django.shortcuts import redirect
from django.core.mail import mail_admins
from django.contrib.auth.models import User
# Create your views here.

class LoginView(View):
    def get(self, request, **kwargs):
        return render(request, "accounts/login.html")

class SignUpView(FormView):
    template_name = "accounts/sign_up.html"
    form_class = SignUpForm

    def form_valid(self, form):
        form.cleaned_data.pop("confirm_password", "None")
        user = User.objects.create(is_active=False, **form.cleaned_data)
        subject = "New user request for activation."
        message = "User with id={} request for activation.".format(user.id)
        mail_admins(subject, message)
        return redirect("/accounts/login/")
