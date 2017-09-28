from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from robjects.models import Robject
from django.core.urlresolvers import reverse


class FunctionalTest(TestCase):
    # DEFAULT SHORTCUT URLS
    ROBJECT_LIST_URL = reverse("projects:robjects:robjects_list", kwargs={
                               "project_name": "test_proj"})
    ROBJECT_DELETE_URL = reverse("projects:robjects:robject_delete", kwargs={
                                 "project_name": "test_proj"})

    def login_default_user(self):
        user = User.objects.create_user(
            username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        return user

    def default_set_up_for_robjects_page(self):
        user = self.login_default_user()
        proj = Project.objects.create(name="project_1")

        return user, proj

    def annonymous_testing_helper(self, requested_url, after_login_url=None):
        """ Helper method to use in annonymous redirections tests.
        """
        proj = Project.objects.create(name="test_proj")
        response = self.client.get(requested_url)

        if not after_login_url:
            after_login_url = requested_url

        self.assertRedirects(
            response,
            reverse("login") + f"?next={after_login_url}"
        )
