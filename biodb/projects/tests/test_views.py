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

class RObjectsListViewTests(TestCase):
    def test_anonymous_user_gets_robjects_page(self):
        Project.objects.create(name="PROJECT_1")
        response = self.client.get("/projects/PROJECT_1/robjects/")
        self.assertEqual(response.status_code, 403)
    def test_render_template_on_get(self):
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/projects/PROJECT_1/robjects/")

        self.assertTemplateUsed(response, "projects/robjects_list.html")

    # def test_list_of_robjects_in_context_as_expected(self):
    #     pass
    # def test_robject_list_is_in_template_context(self):
    #     pass
