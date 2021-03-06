from functional_tests.base import FunctionalTest
from robjects.models import Robject
from django.test import tag
from selenium.common.exceptions import NoSuchElementException


@tag('slow')
class UserGeneratesExcel(FunctionalTest):
    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_slug_helper(self.ROBJECT_EXCEL_URL)

    def test_annonumus_user_visits_robject_excel_page(self):
        self.annonymous_testing_helper(requested_url=self.ROBJECT_EXCEL_URL)

    def test_user_without_project_visit_permission_tries_to_get_excel_raport(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        Robject.objects.create(name='robject', project=proj)
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/excel-raport/")
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(
            error.text,
            "User doesn't have permission: can visit project"
        )

    def test_user_tries_to_generate_report_without_any_selection(self):
        proj, user = self.set_up_robject_list()
        self.browser.get(self.ROBJECT_LIST_URL)
        self.browser.find_element_by_css_selector(".excel-button").click()
        error = self.browser.find_element_by_css_selector(".messages .error")
        self.assertEqual(error.text, "No robject selected!")

        # confirm that message dont shows up when user selects robjects:

        Robject.objects.create(project=proj, name="bla bla")
        self.browser.get(self.ROBJECT_LIST_URL)
        self.browser.find_element_by_css_selector(".robject.checkbox").click()
        self.browser.find_element_by_css_selector(".excel-button").click()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_css_selector(".messages .error")
