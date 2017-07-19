from django.views.generic import View
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
class RedirectView(View):
    def get(self, request, **kwargs):
        return redirect(reverse("login"))
