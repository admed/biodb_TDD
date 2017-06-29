from django.conf.urls import include, url
from django.contrib import admin
from accounts import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'biodb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.WelcomeView.as_view(), name="welcome_page"),
    url(r'^admin/', include(admin.site.urls)),
]
