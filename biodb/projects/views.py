from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
from biodb.mixins import LoginRequiredMixin
# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
