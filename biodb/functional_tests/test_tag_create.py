# import time
# from datetime import datetime
import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from projects.models import Tag
from robjects.models import Robject
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm

class TagCreateTestCase(FunctionalTest):
    def get_tag_create(self, proj):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/create/")

    def test_annonymous_user_visits_tags_list(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # Annonymus user can not visit tag create page.
        self.get_tag_create(proj)
        # He can not enter requested url.
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + f"/accounts/login/?next=/projects/{proj.name}/tags/create/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_tag_cerate_page(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # User gets tag list. He doesn't have project visit permission.
        self.get_tag_create(proj)
        # He sees perrmision denied error.
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(error.text, "403 Forbidden")

    def test_user_seas_statatic_elements_of_page(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISION FOR USR TO PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets tag list. He doesn't have project visit permission.
        self.get_tag_create(proj)
        # He seas satble element of page
        header = self.browser.find_element_by_css_selector("h1")
        self.assertEquals(header.text, "Create Tag:")
        # He seas form to input name of tag.
        form = self.browser.find_element_by_css_selector("p")
        self.assertEquals(form.text, "Name:")
        # He seas link back to sample page.
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Return back to samples page")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/samples/")
