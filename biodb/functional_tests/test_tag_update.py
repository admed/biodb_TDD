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


class TagUpdateTestCase(FunctionalTest):
    def get_tag_update(self, proj, tag):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/{tag.id}/update/")

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_kwarg_helper(self.TAG_EDIT_URL)

    def test_annonymous_user_visits_tags_list(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # CREATE SAMPLE TAG TO UPDATE.
        tag = Tag.objects.create(name="tag")
        # Annonymus user can not visit tag update page.
        self.get_tag_update(proj, tag)
        # He can not enter requested url.
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + f"/accounts/login/?next=/projects/{proj.name}/tags/{tag.id}/update/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_tagupdate(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # CREATE SAMPLE TAG TO UPDATE.
        tag = Tag.objects.create(name="tag")
        # Annonymus user can not visit tag update page.
        self.get_tag_update(proj, tag)
        # time.sleep(10)
        # He sees perrmision denied error.
        error = self.browser.find_element_by_css_selector("h1")
        # self.assertEqual(error.text, "403 Forbidden")

    def test_user_checks_tag_section_header_and_return_link(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE TAG TO UPDATE.
        tag = Tag.objects.create(name="tag", project=proj)
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
        # User gets tag update page.
        self.get_tag_update(proj, tag)
        # He seas header Update Tag.
        header = self.browser.find_element_by_css_selector('h1')
        self.assertEquals(header.text, "Update Tag:")
        # He seas to come back to tag list of project.
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Return back to project tag list")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/")

    def test_user_updates_tag_name(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE TAG TO UPDATE.
        tag = Tag.objects.create(name="tag", project=proj)
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
        # User gets tag update page.
        self.get_tag_update(proj, tag)
        # type correct tag name in name form.
        input_form = self.browser.find_element_by_css_selector("#id_name")
        input_form.clear()
        input_form.send_keys("QWERTY")
        # He clicks save button.
        self.browser.find_element_by_css_selector(
            "input[type='submit']").click()
        # He seas tag updated list.
        tag_element = self.browser.find_element_by_css_selector("li")
        self.assertEqual(tag_element.text, "QWERTY")
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/")
