from django.conf.urls import include, url
from django.contrib import admin
from biodb import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'biodb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.RedirectView.as_view(), name="welcome_page"),
    url(r'^accounts/', include("accounts.urls")),
    url(r'^admin/', include(admin.site.urls)),
]
