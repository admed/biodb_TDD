from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from robjects.models import Robject
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm


class FunctionalTest(TestCase):
    # DEFAULT SHORTCUT URLS
    ROBJECT_LIST_URL = reverse("projects:robjects:robjects_list", kwargs={
                               "project_name": "project_1"})
    ROBJECT_DELETE_URL = reverse("projects:robjects:robject_delete", kwargs={
                                 "project_name": "project_1"})

    def default_set_up_for_projects_pages(self):
        user = User.objects.create_user(
            username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        return user

    def default_set_up_for_robjects_pages(self):
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        assign_perm("can_visit_project", user, proj)

        return user, proj

    def annonymous_testing_helper(self, requested_url, after_login_url=None):
        """ Helper method to use in annonymous redirections tests.
        """
        proj = Project.objects.create(name="project_1")
        response = self.client.get(requested_url)

        if not after_login_url:
            after_login_url = requested_url

        self.assertRedirects(
            response,
            reverse("login") + f"?next={after_login_url}"
        )

    def visit_permission_testing_helper(self, url):
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        error_message = "User doesn't have permission to visit the project."
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>{error_message}</h1>", response.content.decode("utf-8"))

    def other_permission_testing_helper(self, url, error_message):
        user, proj = self.default_set_up_for_robjects_pages()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>{error_message}</h1>", response.content.decode("utf-8"))
