from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
from biodb.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from projects.models import Tag
from django.shortcuts import redirect
from biodb import settings


# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


class TagsListView(ListView):
    model = Tag
    template_name = 'projects/tags_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
