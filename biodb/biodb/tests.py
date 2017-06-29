from django.test import TestCase, Client

class WelcomeViewTests(TestCase):
    def test_uses_welcome_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "biodb/welcome.html")
