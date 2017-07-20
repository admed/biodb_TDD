from django.test import TestCase
from django.contrib.auth.models import User

class RedirectViewTests(TestCase):
    def test_redirect_annonymous_user_to_welcome_page_after_get(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/")

    def test_redirect_logged_user_to_projects_page(self):
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/")
        self.assertRedirects(response, "/projects/")
