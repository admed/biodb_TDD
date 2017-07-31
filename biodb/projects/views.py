from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
from biodb.mixins import LoginRequiredMixin
from django.http import HttpResponse
from projects.models import Robject
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import View
# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


def robjects_list_view(request, project_name):
    if not request.user.is_authenticated():
        raise PermissionDenied
    project = Project.objects.get(name=project_name)
    robject_list = Robject.objects.filter(project=project)
    return render(request, "projects/robjects_list.html",
                  {"robject_list": robject_list})


class SearchRobjectsView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("name")
        queryset = list()

        for robject in Robject.objects.all():
            if query in robject.name:
                queryset.append(robject)
        return render(request, "projects/robjects_list.html",
                      {"robject_list": queryset})
