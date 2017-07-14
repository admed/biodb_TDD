from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
# Create your views here.
class ProjectListView(ListView):
    model = Project
    # def get(self, request, **kwargs):
    #     projects = Project.objects.all()
    #     return render(request, "projects/project_list.html", {"project_list":projects})
