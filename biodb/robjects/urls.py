from django.conf.urls import url
from robjects.views import robjects_list_view, SearchRobjectsView
from django.http import HttpResponse
from robjects.views import RobjectCreateView, NameCreateView, TagCreateView

urlpatterns = [
    url(r"^search/$",
        SearchRobjectsView.as_view(), name="search_robjects"),
    url(r"^$", robjects_list_view, name="robjects_list"),
    url(r"^create/$", RobjectCreateView.as_view(), name="robject_create"),
    url(r"^names-create/$", NameCreateView.as_view(), name="names_create"),
    url(r"^tags-create/$", TagCreateView.as_view(), name="tags_create"),
]
