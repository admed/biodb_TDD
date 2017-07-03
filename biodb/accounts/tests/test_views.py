from django.test import TestCase, Client
from accounts.forms import SignUpForm

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

    def test_form_passed_to_template_context(self):
        response = self.client.get("/accounts/sign-up/")
        self.assertEqual(response.context["form"].__class__, SignUpForm)

    def test_display_errors_when_invalid_form_on_post(self):
        post_data = {
            "username": "",
            "email": "",
            "password": "",
            "confirm": ""
        }
        response = self.client.post("/accounts/sign-up/", post_data)
        self.assertTemplateUsed("accounts/sign-up.html")

        error_msg = "This field is required."
        for form_field in ["username", "email", "password", "confirm_password"]:
            self.assertFormError(response, "form", form_field, error_msg)
