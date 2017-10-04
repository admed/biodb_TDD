from django.contrib.auth.models import User
from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Robject
from robjects.models import Tag
from django.contrib.auth.models import User
from django.test import tag
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
from selenium.webdriver.common.keys import Keys


@tag('slow')
class UserGeneratesExcel(FunctionalTest):
    def test_annonumus_user_visits_robject_excel_page(self):
        # CREATE SAMPLE PROJECT FOR USER.
        proj = Project.objects.create(name="Project_1")
        # He gets wants to visit robjects excel page.
        self.browser.get(
            self.live_server_url +
            f"/projects/{proj.name}/robjects/excel-raport/")
        # He seas Biodb login page.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/robjects/excel-raport/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_robject_PDF_raport(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject', project=proj)
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/excel-raport/")
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(error.text, "403 Forbidden")
