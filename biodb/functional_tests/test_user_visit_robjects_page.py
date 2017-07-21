from functional_tests.base import FunctionalTest
from projects.models import Project
from datetime import datetime
import time
from django.contrib.auth.models import User
from projects.models import Robject

class UserVisitRobjectsPage(FunctionalTest):
    def test_annonymous_user_visit_robjects_page(self):
        # To visit any robjects page, project object needed.
        Project.objects.create(name="PROJECT_1")
        # Anonymous user goes to robjects page. He sees permission denied
        # message
        self.browser.get(self.live_server_url +
                         "/projects/PROJECT_1/robjects/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(body.text, "403 Forbidden")

    def test_logged_user_visit_robjects_page_no_robjects_exists(self):
        # Create user and log him in.
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.login_user(username="USERNAME", password="PASSWORD")
        # Logged user visit robjects page. He sees robjects table. Table has
        # several columns: robject id, robject name, robject create date,
        # robject author.
        self.browser.get(self.live_server_url + "/projects/project_1/robjects")
        header_row = self.browser.find_element_by_id("header_row")
        table_columns = header_row.find_elements_by_tag_name("th")
        table_columns_names = [column.text for column in table_columns]
        self.assertIn("id", table_columns_names)
        self.assertIn("robject", table_columns_names)
        self.assertIn("create by", table_columns_names)
        self.assertIn("modify by", table_columns_names)
        self.assertIn("create date", table_columns_names)
        self.assertIn("author", table_columns_names)

        # Table hasnt any rows
        robject_rows = self.browser.find_elements_by_css_selector(
            ".row.robject")
        self.assertEqual(len(robject_rows), 0)

    # def test_logged_user_visit_robjects_page_robjects_exists_in_projects(self):
    #     self.browser.get(self.live_server_url + "/projects/project_1/robjects")
    #     robject_rows = self.browser.find_elements_by_css_selector(
    #         ".row.robject")
    #     self.assertEqual(len(robject_rows), 3)
    #     for robject in [r1, r2, r3]:
    #         row = robject_rows.find_element_by_class_name(str(robject.id))
    #         self.assertIn("<td>{}</td>".format(robject.id), row.text)
    #         self.assertIn("<td>{}</td>".format(robject.name), row.text)
    #         self.assertIn("<td>{}</td>".format(robject.create_by), row.text)
    #         self.assertIn("<td>{}</td>".format(robject.create_date), row.text)
    #         self.assertIn("<td>{}</td>".format(robject.modify_by), row.text)
    #         self.assertIn("<td>{}</td>".format(robject.author), row.text)
