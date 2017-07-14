from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
# Create your views here.
class ProjectListView(View):
    def get(self, request, **kwargs):
        projects = Project.objects.all()
        return render(request, "projects/project_list.html", {"project_list":projects})
