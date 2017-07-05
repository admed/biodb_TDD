from django.test import TestCase, Client
from accounts.forms import SignUpForm
from django.core import mail
from biodb import settings
from django.contrib.auth.models import User

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

    def test_redirect_when_form_valid(self):
        credentials = {
            "username": "Pope Francis",
            "email": "holy@father.vt",
            "password": "habemus_papam",
            "confirm_password": "habemus_papam"
        }
        response = self.client.post("/accounts/sign-up/", credentials)
        self.assertRedirects(response, "/accounts/login/")

    def test_create_inactive_user_on_form_valid(self):
        credentials = {
            "username": "Pope Francis",
            "email": "holy@father.vt",
            "password": "habemus_papam",
            "confirm_password": "habemus_papam"
        }
        response = self.client.post("/accounts/sign-up/", credentials)
        user = User.objects.last()
        self.assertEqual(user.username, credentials["username"])
        self.assertEqual(user.email, credentials["email"])
        self.assertEqual(user.password, credentials["password"])
        self.assertFalse(user.is_active)

    def test_send_email_on_form_valid(self):
        credentials = {
            "username": "Pope Francis",
            "email": "holy@father.vt",
            "password": "habemus_papam",
            "confirm_password": "habemus_papam"
        }
        response = self.client.post("/accounts/sign-up/", credentials)
        user = User.objects.last()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "[BioDB] New user request for activation."
        )
        self.assertEqual(
            mail.outbox[0].body,
            "User with id={} request for activation.".format(user.id)
        )
        self.assertEqual(
            mail.outbox[0].to,
            [admin_data[1] for admin_data in settings.ADMINS]
        )
