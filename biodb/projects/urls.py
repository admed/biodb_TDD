from django.conf.urls import url
from django.conf.urls import include
from projects.views import ProjectListView
from projects.views import TagsListView
from projects.views import TagsCreateView

app_name = 'projects'
urlpatterns = [
    url(r"^$", ProjectListView.as_view(), name="projects_list"),
    url(r"^(?P<project_name>\w+)/robjects/", include("robjects.urls")),
    url(r"^(?P<project_name>\w+)/samples/", include("samples.urls")),
    url(r"^(?P<project_name>\w+)/tags/", TagsListView.as_view(), name="tag_list"),
<<<<<<< Updated upstream
]
||||||| merged common ancestors
    url(r"^(?P<project_name>\w+)/samples/", include("samples.urls")),
]
=======
    ]
>>>>>>> Stashed changes
