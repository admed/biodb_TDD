from django.test import TestCase
from projects.models import Project
from django.contrib.auth.models import User
class ProjectListViewTestCase(TestCase):
    def test_renders_given_template(self):
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/projects/")
        self.assertTemplateUsed(response, "projects/project_list.html")

    def test_pass_project_list_to_template_context(self):
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/projects/")
        self.assertIn("project_list", response.context)

    def test_get_project_list_from_db(self):
        p1 = Project.objects.create(name="project_1")
        p2 = Project.objects.create(name="project_2")
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/projects/")
        self.assertIn(p1, response.context["project_list"])
        self.assertIn(p2, response.context["project_list"])

    def test_login_requirement(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, 403)
