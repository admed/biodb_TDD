from django.test import TestCase, Client
from accounts.forms import SignUpForm
from django.contrib.auth.models import User
from django import forms

class SignUpFormTests(TestCase):
    def assert_custom_field_attribute(self, field, attr, value):
        f = SignUpForm()
        field_id = f.fields[field].widget.attrs[attr]
        self.assertEqual(field_id, value)

    def test_custom_username_field_id(self):
        self.assert_custom_field_attribute("username", "id", "username_input")

    def test_custom_email_field_id(self):
        self.assert_custom_field_attribute("email", "id", "email_input")

    def test_custom_password_field_id(self):
        self.assert_custom_field_attribute("password", "id", "password_input")

    def test_custom_confirm_password_field_id(self):
        self.assert_custom_field_attribute("confirm_password", "id", "confirm_input")

    def test_custom_username_field_placeholder(self):
        self.assert_custom_field_attribute("username", "placeholder", "username")

    def test_custom_email_field_placeholder(self):
        self.assert_custom_field_attribute("email", "placeholder", "email")

    def test_custom_password_field_placeholder(self):
        self.assert_custom_field_attribute("password", "placeholder", "password")

    def test_custom_confirm_password_field_placeholder(self):
        self.assert_custom_field_attribute("confirm_password", "placeholder", "confirm password")

    def test_validate_username_duplication(self):
        u = User.objects.create_user(username="Julius Cesar")
        f = SignUpForm({"username":"Julius Cesar"})
        self.assertFalse(f.is_valid())
        self.assertIn(
            "User with such username or email already exists",
            f.errors["__all__"]
        )

    def test_validate_email_duplication(self):
        u = User.objects.create_user(username="Julius Cesar",
                                                      email="veni_vidi@vici.it")
        f = SignUpForm({"email":"veni_vidi@vici.it"})
        self.assertFalse(f.is_valid())
        self.assertIn(
            "User with such username or email already exists",
            f.errors["__all__"]
        )

    def test_validate_passwords_doesnt_match(self):
        f = SignUpForm({
            "password":"password_A",
            "confirm_password":"password_B"
        })
        self.assertIn(
            "Passwords doesn't match.",
            f.errors["__all__"]
        )
