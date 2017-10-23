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


class TagListTestCase(FunctionalTest):
    def get_tag_list(self, proj):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/")

    def test_annonymous_user_visits_tags_list(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # Annonymus user can not visit tag list page.
        self.get_tag_list(proj)
        # He can not enter requested url.
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/tags/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_tag_list(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # User gets tag list. He doesn't have project visit permission.
        self.get_tag_list(proj)
        # He sees perrmision denied error.
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(error.text, "403 Forbidden")

    def test_user_checks_tag_section_header_and_return_link(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets sample list.
        self.get_tag_list(proj)
        # He seas header of the list 'Tag'
        header = self.browser.find_element_by_css_selector('h1')
        self.assertEquals(header.text, "Tags:")
        # He seas to come back to robjects list of project
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Return back to project robjects page")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/robjects/")

    def test_user_checks_return_link_to_projects_project(self):
        # CREATE SAMPLE PROJECT AND USER
        usr = self.login_user("USERNAME", "PASSWORD")
        proj = Project.objects.create(name="project_test")
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets sample list.
        self.get_tag_list(proj)
        # He seas to come back to robjects list of project
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Return back to project robjects page")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/robjects/")

    def test_user_checks_empty_tag_section(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets tag list page.
        self.get_tag_list(proj)
        empty_list_message = self.browser.find_element_by_css_selector('span')
        self.assertEqual(empty_list_message.text,
                         "There are no tags attached to this project.")

    def test_user_seas_one_tag_in_project_tag_list(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECTS
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE TAGS TO PROJECTS
        tag = Tag.objects.create(name='tag_1', project=proj)
        self.get_tag_list(proj)
        # User seas list of tags.
        list_of_tags = self.browser.find_elements_by_css_selector('li')
        # He seas that list has one tag in it.
        self.assertEqual(len(list_of_tags), 1)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_css_selector(".empty_tag_msg")

    def test_user_creates_several_tags_for_several_projects(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj1 = self.project_set_up_using_default_data()
        # CRREATE ANOTHER PORJECT FOR THIS USER
        proj2 = Project.objects.create(name='project_2')
        # ASSIGN PERMISSION TO PROJECTS
        assign_perm("projects.can_visit_project", usr, proj1)
        assign_perm("projects.can_visit_project", usr, proj2)
        # CREATE TAGS TO PROJECTS
        tag1 = Tag.objects.create(name='t_1', project=proj1)
        tag2 = Tag.objects.create(name='t_2', project=proj2)
        tag3 = Tag.objects.create(name='t_3', project=proj2)
        tag4 = Tag.objects.create(name='t_4', project=proj1)
        # User gets tag list page.
        self.get_tag_list(proj1)
        # User seas list of tags.
        list_of_tags = self.browser.find_elements_by_css_selector('li')
        # He seas that list has two tags in it.
        self.assertEqual(len(list_of_tags), 2)

    def test_user_clicks_tag_name_link_for_updating(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj1 = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj1)
        # CREATE TAG TO PROJECT
        tag1 = Tag.objects.create(name='t_1', project=proj1)
        # User gets tag list page.
        self.get_tag_list(proj1)
        # User seas list of tags.
        tag = self.browser.find_element_by_css_selector('.t_1-update')
        tag.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj1.name}/tags/{tag1.id}/update/")

    def test_user_checks_remove_icon_redirects_to_tag_delete(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECTS
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE TAGS TO PROJECTS
        tag = Tag.objects.create(name='tag_1', project=proj)
        self.get_tag_list(proj)
        # User seas list of tags and remove
        button = self.browser.find_element_by_css_selector('i')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/tags/{tag.id}/delete/")
