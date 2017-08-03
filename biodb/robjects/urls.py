from django.conf.urls import url
from robjects.views import robjects_list_view, SearchRobjectsView
urlpatterns = [
    url(r"^search/$",
        SearchRobjectsView.as_view(), name="search_robjects"),
    url(r"^$", robjects_list_view, name="robjects_list"),
]
