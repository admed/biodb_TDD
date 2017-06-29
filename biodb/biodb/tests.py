from django.test import TestCase

class RedirectViewTests(TestCase):
    def test_redirect_annonymous_user_to_welcome_page_after_get(self):
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/")
