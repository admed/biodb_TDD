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


class UserGeneratePDFRaport(FunctionalTest):
    def test_annonymous_user_visits_pdf_page(self):
        # CREATE SAMPLE PROJECT.
        proj = Project.objects.create(name="project_1")
        # Annonymus user can not visit raport pdf page.
        self.annonymous_user(f"/projects/{proj.name}/robjects/PDF-raport/")

    #
    #
    # def test_logged_user_checks_robject_name(self):
    #     # Create sample project and robject
    #     usr, proj = self.project_set_up_using_default_data()
    #
    #     # Create sample robjects basic informations.
    #     robj1 = Robject.objects.create(
    #         author=usr, project=proj, name="robject_1")
    #
    #     # User goes directly to robject raport_pdf page
    #     self.browser.get(
    #         self.live_server_url +
    #         f"/projects/{proj.name}/robjects/raport_pdf/")
    #     time.sleep(1)
    #     content = self.wait_for(
    #         lambda: self.browser.find_element_by_css_selector(".textLayer"))
    #     self.assertIn('robject_1', content.text)
    #
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
