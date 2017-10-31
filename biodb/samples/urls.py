from django.conf.urls import url
from samples.views import SampleListView
from samples.views import SampleDetailView

app_name = "samples"
urlpatterns = [
    url(r"^$", SampleListView.as_view(), name="sample_list"),
    url(r'^(?P<sample_id>[0-9]+)/$', SampleDetailView.as_view(),
        name='sample_details'),
]
