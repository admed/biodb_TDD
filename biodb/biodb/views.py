from django.views.generic import View
from django.shortcuts import redirect
class RedirectView(View):
    def get(self, request, **kwargs):
        return redirect("/accounts/login/")
