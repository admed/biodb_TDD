from django.test import TestCase
from projects.models import Project
class ProjectListViewTestCase(TestCase):
    def test_renders_given_template(self):
        response = self.client.get("/projects/")
        self.assertTemplateUsed(response, "projects/project_list.html")
    def test_pass_project_list_to_template_context(self):
        response = self.client.get("/projects/")
        self.assertIn("project_list", response.context)
    def test_get_project_list_from_db(self):
        p1 = Project.objects.create(name="project_1")
        p2 = Project.objects.create(name="project_2")
        response = self.client.get("/projects/")
        self.assertIn(p1, response.context["project_list"])
        self.assertIn(p2, response.context["project_list"])
