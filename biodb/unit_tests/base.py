from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from robjects.models import Robject
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
import urlparse


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

    ROBJECT_HISTORY_URL = reverse(
        "projects:robjects:robject_history",
        kwargs={"project_name": "project_1", "robject_id": 1})

    TAG_CREATE_URL = reverse("projects:tag_create", kwargs={
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

    def annonymous_testing_helper(self, requested_url):
        """ Helper method to use in annonymous redirections tests.
        """
        proj = Project.objects.create(name="project_1")
        response = self.client.get(requested_url)

        self.assertRedirects(
            response,
            reverse("login") + f"?next={requested_url}")

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
        robj = Robject.objects.create(name="robject_1", project=proj)
        for perm in preassigned_perms:
            assign_perm(perm, user, proj)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>{error_message}</h1>", response.content.decode("utf-8"))

    def not_matching_url_slug_helper(self, requested_url):
        match = resolve(requested_url)
        kwargs = match.kwargs
        self.default_set_up_for_projects_pages()

        for name in kwargs:
            amend_kwargs = dict(kwargs)
            if name == "project_name":
                amend_kwargs[name] = "random_project"
            else:
                amend_kwargs[name] = 123456789
            new_path = reverse(match.app_name + ":" +
                               match.url_name, kwargs=amend_kwargs)
            response = self.client.get(new_path)
            self.assertIn("<h1>Not Found</h1>", response.content)
            self.assertIn(
                f"<p>The requested URL {new_path} was not found on this server.</p>",
                response.content)
