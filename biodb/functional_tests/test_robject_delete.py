from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Robject
from django.contrib.auth.models import User


class RobjectDeleteTestCase(FunctionalTest):
    def test_user_notice_checkbox_column_in_robject_table(self):
        # SET UP
        proj, user = self.set_up_robject_list()

        # CREATE SAMPLE ROBJECTS
        for name in ["r1", "r2", "r3"]:
            Robject.objects.create(project=proj, name=name)

        # User goes to robject page
        self.browser.get(self.default_url_robject_list())

        # He notice checkbox input in the first cell in table header.
        table_header = self.browser.find_element_by_css_selector("#header_row")
        table_header.find_element_by_css_selector(
            "th:first-child input[type='checkbox'].select-all")

        # User notice checkbox input at the begining of every row and one main
        # checkbox in table header.
        rows = self.browser.find_elements_by_css_selector(".row")
        for row in rows:
            row.find_element_by_css_selector(
                "td:first-child input[type='checkbox']")
