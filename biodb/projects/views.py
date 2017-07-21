from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
from biodb.mixins import LoginRequiredMixin
from django.http import HttpResponse
# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


def robjects_list_view(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    return render(request, "projects/robjects_list.html")
