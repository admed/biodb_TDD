from django.conf.urls import include, url
from accounts import views
from django.contrib.auth import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'biodb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^sign-up/$', views.SignUpView.as_view(), name="sign_up")

]
