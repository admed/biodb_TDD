from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from secrets import choice


@tag('slow')
class ProjectsPageTestCase(FunctionalTest):
    def setUp(self):
        super(ProjectsPageTestCase, self).setUp()
        # project names are create randomly to prove that names in template
        # comes from db
        self.project_1 = Project.objects.create(
            name="project_" + str(choice(range(2, 100))))
        self.project_2 = Project.objects.create(
            name="project_" + str(choice(range(2, 100))))

    def test_login_required(self):
        self.annonymous_testing_helper(self.PROJECT_LIST_URL)

    def test_user_look_around_projects_page(self):
        # Create and log in user.
        self.login_user(username="USERNAME", password="PASSWORD")
        # User visits projects page of BioDB app. He sees unordered list of
        # links with projects names.
        self.browser.get(self.live_server_url + "/projects/")
        projects_list = self.browser.find_element_by_css_selector(
            "ul.projects_list")
        projects = projects_list.find_elements_by_css_selector("li.project a")
        self.assertIn(self.project_1.name, [p.text for p in projects])
        self.assertIn(self.project_2.name, [p.text for p in projects])

    def test_user_goes_to_certain_project(self):
        # Create and log in user.
        User.objects.create_user(
            username="USERNAME", password="PASSWORD")
        self.login_user(username="USERNAME", password="PASSWORD")
        # User visits projects page of BioDB app. He clicks one of projects
        # links. He is redirected to /projects/<project_name>/robjects/.
        self.browser.get(self.live_server_url + "/projects/")
        link = self.browser.find_element_by_css_selector("li:first-child a")
        link.click()

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/projects/{}/robjects/".format(
                self.project_1.name)
        )
