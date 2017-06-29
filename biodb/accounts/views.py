from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class LoginView(View):
    def get(self, request, **kwargs):
        return render(request, "accounts/login.html")
