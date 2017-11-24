from functional_tests.base import FunctionalTest
from django.test import tag
from robjects.models import Robject


@tag('slow')
class UserVisitRobjectsPage(FunctionalTest):
    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_slug_helper(self.ROBJECT_LIST_URL)

    def test_annonymous_user_visit_robjects_page(self):
        self.annonymous_testing_helper(self.ROBJECT_LIST_URL)

    def test_user_without_visit_perm_visit_robjects_page(self):
        self.permission_view_testing_helper(self.ROBJECT_LIST_URL)

    def test_logged_user_visit_robjects_page___no_robjects_exists(self):
        proj, usr = self.default_set_up_for_robjects_pages()

        # Logged user visit robjects page. He sees robjects table. Table has
        # several columns: robject id, robject name, robject create date,
        # robject author.
        self.browser.get(
            self.live_server_url + f"/projects/{proj.name}/robjects")
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
        proj, usr = self.default_set_up_for_robjects_pages()

        # Create sample robjects.
        robj1 = Robject.objects.create(
            author=usr, project=proj, name="robject_1")
        robj2 = Robject.objects.create(
            author=usr, project=proj, name="robject_2")
        robj3 = Robject.objects.create(
            author=usr, project=proj, name="robject_3")

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
            row = self.browser.find_element_by_class_name(robject.name)
            self.assertIn(str(robject.id), row.text)
            self.assertIn(str(robject.author), row.text)
            # check if name is in right col
            name_col = row.find_elements_by_tag_name("td")[2]
            self.assertIn(robject.name, name_col.text)
            # check if clicking name redirect you to details page
            expected_url = self.live_server_url + \
                f"/projects/{proj.name}/robjects/{robject.pk}/details/"
            # get link
            details_link = name_col.find_element_by_link_text(robject.name)
            # click link
            details_link.click()
            self.assertEqual(self.browser.current_url, expected_url)
            # go back to list of robjects
            self.browser.get(self.live_server_url + "/projects/project_1/robjects")
