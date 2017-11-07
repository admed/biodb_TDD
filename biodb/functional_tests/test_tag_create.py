import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Tag
from robjects.models import Robject
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm


class TagCreateTestCase(FunctionalTest):
    def get_tag_create(self, proj):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/create/")

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_kwarg_helper(self.TAG_CREATE_URL)

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
        self.assertEqual(
            error.text, "User doesn't have permission: can visit project")

    def test_user_seas_statatic_elements_of_page(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISION FOR USR TO PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
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
        self.assertEqual(link.text, "Return back to projects tag page")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/")

    def test_user_creates_tag(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISION FOR USR TO PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
        # User gets tag list. He doesn't have project visit permission.
        self.get_tag_create(proj)
        # He input tah name into form.
        self.browser.find_element_by_css_selector("#id_name").send_keys("tag")
        # He clicks save button.
        self.browser.find_element_by_css_selector(
            "input[type='submit']").click()
        # He seas tag created in tag list.
        tags_list = self.browser.find_elements_by_css_selector("li")
        self.assertEquals(len(tags_list), 1)

    def test_user_wants_to_create_tag_for_not_existing_project(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISION FOR USR TO PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets undefined projects create tag page. Server throws error.
        request_url = "/projects/random_project/tags/create/"
        self.browser.get(self.live_server_url + request_url)
        error_header = self.browser.find_element_by_css_selector("h1")
        error_text = self.browser.find_element_by_css_selector("p")
        self.assertEqual(error_header.text, "Not Found")
        self.assertEqual(error_text.text,
                         f"The requested URL {request_url} was not found on this server.")
