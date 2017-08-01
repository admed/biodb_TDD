from django.conf.urls import url
from projects.views import ProjectListView
from projects.views import robjects_list_view, SearchRobjectsView
urlpatterns = [
    url(r"^$", ProjectListView.as_view(), name="projects_list"),
    url(r"^(\w+)/robjects/$", robjects_list_view, name="robjects_list"),
    url(r"^(\w+)/robjects/search/$",
        SearchRobjectsView.as_view(), name="search_robjects")
]
