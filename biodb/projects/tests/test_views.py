# from django.contrib.auth.models import User
# from django.test import TestCase
from projects.models import Project
from unit_tests.base import FunctionalTest
from guardian.shortcuts import assign_perm


class ProjectListViewTestCase(FunctionalTest):
    def test_renders_given_template(self):
        self.login_default_user()
        response = self.client.get("/projects/")
        self.assertTemplateUsed(response, "projects/project_list.html")

    def test_pass_project_list_to_template_context(self):
        self.login_default_user()
        response = self.client.get("/projects/")
        self.assertIn("project_list", response.context)

    def test_get_project_list_from_db(self):
        proj1 = Project.objects.create(name="project_1")
        proj2 = Project.objects.create(name="project_2")
        self.login_default_user()
        response = self.client.get("/projects/")
        self.assertIn(proj1, response.context["project_list"])
        self.assertIn(proj2, response.context["project_list"])

    def test_login_requirement(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 403)


class TagListViewTestCase(FunctionalTest):
    def test_anonymous_user_is_redirected_to_login_page(self):
        proj = Project.objects.create(name='Project_1')
        response = self.client.get(f"/projects/{proj.name}/tags/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/projects/{proj.name}/tags/')

    def test_template_used(self):
        user = self.login_default_user()
        proj = Project.objects.create(name='Project_1')
        assign_perm("projects.can_visit_project", user, proj)
        response = self.client.get(f"/projects/{proj.name}/tags/")
        self.assertTemplateUsed(response, "projects/tags_list.html")

    def test_user_without_permision_seas_permission_denied(self):
        self.login_default_user()
        proj = Project.objects.create(name='Project_1')
        response = self.client.get(f"/projects/{proj.name}/tags/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("<h1>403 Forbidden</h1>",
                         response.content.decode("utf-8"))
