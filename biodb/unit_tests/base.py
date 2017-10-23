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
    ROBJECT_EDIT_URL = reverse("projects:robjects:robject_edit", kwargs={
        "project_name": "project_1",
        "robject_id": 1
    })

    ROBJECT_EXCEL_URL = reverse("projects:robjects:raport_excel", kwargs={
        "project_name": "project_1"})

    def default_set_up_for_projects_pages(self):
        user = User.objects.create_user(
            username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        return user

    def default_set_up_for_robjects_pages(self):
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        assign_perm("projects.can_visit_project", user, proj)

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
            reverse("login") + f"?next={after_login_url}")

    def permission_testing_helper(self, url, error_message, preassigned_perms=[]):
        """ Helper method to use in perrmissions tests.

            Args:
                url: address of requested view
                error_message: message you expect to see when permission
                    valuation fails
                preassigned_perms: list of permissions already attached to user 
        """
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        for perm in preassigned_perms:
            assign_perm(perm, user, proj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>{error_message}</h1>", response.content.decode("utf-8"))
