from django.test import TestCase, Client

# Create your tests here.

class LoginViewTests(TestCase):
    def test_uses_welcome_template(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

class SignUpViewTests(TestCase):
    def test_render_valid_template_on_get(self):
        response = self.client.get("/accounts/sign-up/")
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed(response, "accounts/sign_up.html")
