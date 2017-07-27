# import time
# from datetime import datetime
from django.contrib.auth.models import User
from functional_tests.base import FunctionalTest
from projects.models import Project
from datetime import datetime
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

    def test_logged_user_visit_robjects_page___no_robjects_exists(self):
        # Create user and log him in.
        u = User.objects.create_user(username="USERNAME", password="PASSWORD")
        self.login_user(username="USERNAME", password="PASSWORD")
        # Craete sample project
        p = Project.objects.create(name="project_1")
        # Logged user visit robjects page. He sees robjects table. Table has
        # several columns: robject id, robject name, robject create date,
        # robject author.
        self.browser.get(self.live_server_url + "/projects/project_1/robjects")
        header_row = self.browser.find_element_by_id("header_row")
        table_columns = header_row.find_elements_by_tag_name("th")
        table_columns_names = [column.text for column in table_columns]

        self.assertIn("id", table_columns_names)
        self.assertIn("name", table_columns_names)
        self.assertIn("author", table_columns_names)
        self.assertIn("create by", table_columns_names)
        self.assertIn("create date", table_columns_names)
        self.assertIn("modify by", table_columns_names)

        # Table hasnt any rows
        robject_rows = self.browser.find_elements_by_css_selector(
            ".row.robject")
        self.assertEqual(len(robject_rows), 0)

    def test_logged_user_visit_robjects_page___robjects_exists_in_project(self):
        # Create user and log him in.
        usr = self.login_user(username="USERNAME", password="PASSWORD")

        # Create sample project
        proj = Project.objects.create(name="project_1")

        # Create sample robjects.
        robj1 = Robject.objects.create(author=usr, project=proj)
        robj2 = Robject.objects.create(author=usr, project=proj)
        robj3 = Robject.objects.create(author=usr, project=proj)

        # Logged user goes to project_1's robjects page. He knows that this
        # project contains several robjects. He sees table of rows. Each row
        # contains data of singe robject from this project.

        self.browser.get(self.live_server_url + "/projects/project_1/robjects")
        # rows has class names : "row robject_<robject pk>"
        # capture all rows
        robject_rows = self.browser.find_elements_by_css_selector(
            ".row")
        self.assertEqual(len(robject_rows), 3)

        for robject in [robj1, robj2, robj3]:
            # capture specific row
            row = self.browser.find_element_by_class_name(
                "robject_" + str(robject.id))
            self.assertIn(str(robject.id), row.text)
            self.assertIn(str(robject.author), row.text)


class SearchEngineTests(FunctionalTest):
    def test_user_perform_search_based_on_whole_robj_name_and_find_robject(self):
        # Log user.
        user = self.login_user("USERNAME", "PASSWORD")

        # Create project.
        project = Project.objects.create(name="project_1")

        # Create sample robjects.
        Robject.objects.create(name="robject_1", project=project)
        Robject.objects.create(name="robject_2", project=project)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         "/projects/project_1/robjects/")

        # He sees two robjects in table.
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(".row.robject_1"))
        self.browser.find_element_by_css_selector(".row.robject_2")

        # User wants to test search tool. He looks for search form, input and
        # button.
        search_form = self.browser.find_element_by_id("search_form")
        search_input = self.browser.find_element_by_id("search_input")
        search_button = self.browser.find_element_by_id("search_button")

        # User enter name of one robject and expect to see only this robject in
        # table.
        search_input.send_keys("robject_1")
        search_button.click()

        rows = self.browser.find_elements_by_css_selector(".row")
        self.assertEqual(len(rows), 1)

        self.browser.find_elements_by_css_selector(".robject_1")

    def test_user_perform_search_based_on_part_of_word(self):
        pass

    def test_user_limits_number_of_fields_to_search(self):
        pass

    def test_user_narrows_the_search_to_the_date_range(self):
        pass
