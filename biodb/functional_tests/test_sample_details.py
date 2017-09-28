import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
# from projects.models import Tag
from robjects.models import Robject
from samples.models import Sample
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm


class TestUserVisitsSampleDetails(FunctionalTest):
    def test_annonymous_user_visits_samples_details(self):
        # CREATE SAMPLE PROJECT BASIC INFORMATIONS.
        proj = Project.objects.create(name="project_1")
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE SAMPLE FOR PROJECT.
        samp = Sample.objects.create(code='sample_1', robject=robj)
        # Annonymus user want to visit sample detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/samples/{samp.id}/")
        current_url = self.browser.current_url
        # Annonymus user is redirected to login page.
        expected_url = self.live_server_url + f"/accounts/login/?next=/projects/{proj.name}/samples/{samp.id}/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_permission_wants_to_vist_sample_detail_page(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE SAMPLE FOR PROJECT.
        samp = Sample.objects.create(code='sample_1', robject=robj)
        # User want to visit sample detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/samples/{samp.id}/")
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(error.text, "403 Forbidden")

    def test_user_with_permission_seas_single_sample_detail_page_and_checks_static_elements(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # SET USER PERMISSION FOR PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE SAMPLE FOR PROJECT.
        samp = Sample.objects.create(code='sample_1', robject=robj)
        # User want to visit sample detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/samples/{samp.id}/")
        # User seas header which is sample code.
        header_content = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header_content.text, "sample_1")
        # User also seas return to samples table link.
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Back to sample table")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/samples/")

    def test_user_checks_sample_details_on_page(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # SET USER PERMISSION FOR PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE AND DETAILS.
        samp = Sample.objects.create(code='sample_1',
                                     robject=robj,
                                     notes='Some Sample Notes',
                                     form='solid, 1px',
                                     source='SourceCode',
                                     status=7
                                     )

        # User want to visit sample detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/samples/{samp.id}/")

        # User seas list of details.
        detail_list = self.browser.find_elements_by_css_selector('li')
        self.assertIn("robject_1", detail_list[0].text)
        self.assertIn("Some Sample Notes", detail_list[1].text)
        self.assertIn("solid, 1px", detail_list[2].text)
        self.assertIn("SourceCode", detail_list[3].text)
        self.assertIn("Production", detail_list[4].text)

    def test_user_creates_several_samples_for_projects_and_checks_one_sample_details(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # SET USER PERMISSION FOR PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE AND DETAILS.
        samp1 = Sample.objects.create(code='sample_1',
                                      robject=robj,
                                      notes='Some Sample Notes',
                                      form='solid 1px',
                                      source='SourceCode',
                                      status=7
                                      )

        # CREATE SECOND SAMPLE AND DETAILS.
        samp2 = Sample.objects.create(code='sample_2',
                                      robject=robj,
                                      notes='Some Other Sample Notes',
                                      form='2px solid #ccc',
                                      source='source .bashrc',
                                      status=8
                                      )

        # User want to visit sample detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/samples/{samp2.id}/")
        # User seas list of details for second sample.
        detail_list = self.browser.find_elements_by_css_selector('li')
        self.assertIn("robject_1", detail_list[0].text)
        self.assertIn("Some Other Sample Notes", detail_list[1].text)
        self.assertIn("2px solid #ccc", detail_list[2].text)
        self.assertIn("source .bashrc", detail_list[3].text)
        self.assertIn("Quality COntrol", detail_list[4].text)
