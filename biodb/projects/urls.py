from django.conf.urls import url
from django.conf.urls import include
from projects.views import ProjectListView

app_name = 'projects'
urlpatterns = [
    url(r"^$", ProjectListView.as_view(), name="projects_list"),
    url(r"^(?P<project_name>\w+)/robjects/", include("robjects.urls")),
    url(r"^(?P<project_name>\w+)/samples/", include("samples.urls")),
]
