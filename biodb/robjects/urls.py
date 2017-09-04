from django.conf.urls import url
from robjects.views import robjects_list_view, SearchRobjectsView
from django.http import HttpResponse
from robjects.views import robject_create_view
from robjects.views import NameCreateView

urlpatterns = [
    url(r"^search/$",
        SearchRobjectsView.as_view(), name="search_robjects"),
    url(r"^$", robjects_list_view, name="robjects_list"),
    url(r"^create/$", robject_create_view, name="robject_create"),
    url(r"^names-create/$", NameCreateView.as_view(), name="names_create")
]
