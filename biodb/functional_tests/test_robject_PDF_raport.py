import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from projects.models import Tag
from robjects.models import Robject
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm


class UserGeneratePDFRaport(FunctionalTest):
    def test_annonymous_user_visits_pdf_page(self):
        # CREATE SAMPLE PROJECT.
        proj = Project.objects.create(name="project_1")
        # He can not enter requested url.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/PDF-raport/")
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/robjects/PDF-raport/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_robject_PDF_raport(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject', project=proj)
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/PDF-raport/")
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/robjects/PDF-raport/"
        self.assertEqual(current_url, expected_url)

    def test_logged_user_checks_robject_name(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject', project=proj)
        # ASSIGN USER PERMISSION TO PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/PDF-raport/")
        current_url = self.browser.current_url
        # User vaits for raport to load
        time.sleep(10)
        content = self.wait_for(
            lambda: self.browser.find_element_by_css_selector(".textLayer"))
        self.assertIn('robject_1', content.text)
    
    # def test_logged_user_export_all_robjects_not_checking_any_box(self):
    #     # Create sample project and robject
    #     usr, proj = self.project_set_up_using_default_data()
    #
    #     # Create sample robjects basic informations.
    #     robj1 = Robject.objects.create(
    #         author=usr, project=proj, name="robject_1")
    #     robj2 = Robject.objects.create(
    #         author=usr, project=proj, name="robject_2")
    #     robj3 = Robject.objects.create(
    #         author=usr, project=proj, name="robject_3")
    #
    #     # User goes directly to robject raport_pdf page
    #     self.browser.get(
    #         self.live_server_url +
    #         f"/projects/{proj.name}/robjects/")
    #     checkboxes = self.find_elements_by_name("checkbox")
    #     for box in checkboxes[:2]:
    #         print(box.id)
