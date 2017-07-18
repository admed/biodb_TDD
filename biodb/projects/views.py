from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
# Create your views here.
class ProjectListView(ListView):
    model = Project

    def dispatch(self, request, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        return super(ProjectListView, self).get(request, **kwargs)
