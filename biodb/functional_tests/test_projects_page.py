from functional_tests.base import FunctionalTest
from projects.models import Project
import random as rd
class ProjectsPageTestCase(FunctionalTest):
    def setUp(self):
        super(ProjectsPageTestCase, self).setUp()
        # project names are create randomly to prove that names in template
        # comes from db
        self.project_1 = Project.objects.create(
                                         name="project_"+str(rd.randint(0,100)))
        self.project_2 = Project.objects.create(
                                         name="project_"+str(rd.randint(0,100)))

    def test_user_look_around_projects_page(self):
        # User visits projects page of BioDB app. He sees unordered list of
        # links with projects names.
        self.browser.get(self.live_server_url + "/projects/")
        projects_list = self.browser.find_element_by_css_selector(
                                                             "ul.projects_list")
        projects = projects_list.find_elements_by_css_selector("li.project a")
        self.assertIn(self.project_1.name, [p.text for p in projects])
        self.assertIn(self.project_2.name, [p.text for p in projects])

    def test_user_goes_to_certain_project(self):
        pass
