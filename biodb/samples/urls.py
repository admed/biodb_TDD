from django.conf.urls import url
from django.conf import settings
from django.conf.urls import include
from samples.views import SampleListView

app_name = "samples"
urlpatterns = [
    url(r"^$", SampleListView.as_view(), name="sample_list"),
    ]
