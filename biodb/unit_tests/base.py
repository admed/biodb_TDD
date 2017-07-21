from django.test import TestCase
from django.contrib.auth.models import User


class FunctionalTest(TestCase):
    def login_default_user(self):
        user = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        return user
