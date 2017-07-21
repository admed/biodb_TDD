from django.test import TestCase
from projects.models import Project
from django.contrib.auth.models import User
from projects.models import Robject

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
        Project.objects.create(name="PROJECT_1")
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        response = self.client.get("/projects/PROJECT_1/robjects/")

        self.assertTemplateUsed(response, "projects/robjects_list.html")

    def test_view_create_list_of_robjects_and_pass_it_to_context(self):
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.client.login(username="USERNAME", password="PASSWORD")
        p1 = Project.objects.create(name="project_1")
        p2 = Project.objects.create(name="project_2")
        r1 = Robject.objects.create(author=u, project=p1)
        r2 = Robject.objects.create(author=u, project=p1)
        r3 = Robject.objects.create(author=u, project=p2)
        response = self.client.get("/projects/project_1/robjects/")
        self.assertIn(r1, response.context["robject_list"])
        self.assertIn(r2, response.context["robject_list"])
        response = self.client.get("/projects/project_2/robjects/")
        self.assertIn(r3, response.context["robject_list"])

    # def test_robject_list_is_in_template_context(self):
    #     pass
