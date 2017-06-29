from django.views.generic import View
from django.shortcuts import render

class WelcomeView(View):
    def get(self, request, **kwargs):
        return render(request, "biodb/welcome.html")
