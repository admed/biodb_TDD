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


class TagDeleteTestCase(FunctionalTest):
    def get_tag_delete(self, proj, tag):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/{tag.id}/delete/")

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_slug_helper(self.TAG_DELETE_URL)

    def test_annonymous_user_visits_tags_delete(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # CREATE SAMPLE TAG TO DELETE .
        tag = Tag.objects.create(name="tag", project=proj)
        # Annonymus user can not visit tag delete page.
        self.get_tag_delete(proj, tag)
        # He can not enter requested url.
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/tags/{tag.id}/delete/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_tagupdate(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # CREATE SAMPLE TAG TO DETELE..
        tag = Tag.objects.create(name="tag", project=proj)
        # Annonymus user can not visit tag delete page.
        self.get_tag_delete(proj, tag)
        # time.sleep(10)
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/tags/{tag.id}/delete/"
        self.assertEqual(current_url, expected_url)

    def test_user_checks_tag_section_header_and_return_link(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE TAG TO DELETE.
        tag = Tag.objects.create(name="tag", project=proj)
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
        # User gets tag delete page.
        self.get_tag_delete(proj, tag)
        # He seas header Update Tag.
        header = self.browser.find_element_by_css_selector('p')
        self.assertEquals(header.text, "Are you sure you want to delete tag?")
        # He seas to come back to tag list of project.
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Return back to project tag page")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/")

    def test_user_deletes_tag(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE TAG TO DELETE..
        tag = Tag.objects.create(name="tag", project=proj)
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        assign_perm("projects.can_modify_project", usr, proj)
        # User gets tag delete page.
        self.get_tag_delete(proj, tag)
        # type correct tag name in name form.
        # He clicks save button.
        self.browser.find_element_by_css_selector(
            "input[type='submit']").click()
        # He seas seas that tag was deleted.
        tag_element = self.browser.find_elements_by_css_selector("li")
        self.assertEqual(len(tag_element), 0)
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/")
