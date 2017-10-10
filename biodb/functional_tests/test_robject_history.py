from django.test import tag
from functional_tests.base import FunctionalTest
from robjects.models import Robject


@tag('slow')
class RobjectHistoryTestCase(FunctionalTest):
    def get_robject_history_url(self, proj, robj):
        """Method returning History url of robject"""
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/{robj.pk}/history/")

    def test_annonymous_user_visit_history_page(self):
        pass

    def test_user_visit_history_for_created_robject(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject
        robject, created = Robject.objects.get_or_create(
            name='robject_1', project=proj, create_by=user)
        # User visits history page of the robject
        self.get_robject_history_url(proj, robject)
        # expected user url
        expected_url = self.live_server_url + \
            f"/projects/{proj.name}/robjects/{robject.pk}/history/"
        # check if urls match
        self.assertEqual(self.browser.current_url, expected_url)
        # user see the table
        table = self.browser.find_element_by_css_selector('table')
        # user see the heder row and one row with data
        rows = table.find_elements_by_css_selector("tr")
        self.assertEqual(len(rows), 2)
        # the're five columns in table
        header_cols = rows[0].find_elements_by_css_selector("th")
        self.assertEqual(len(header_cols), 5)
        # user checking the columns names
        expected_table_heders = ["Version", "Type",	"Changed by",
                                 "Modyfication date", "Changes"]
        table_headers = [col.text for col in header_cols]
        self.assertSequenceEqual(expected_table_heders, table_headers)
        # user looking into data, only creation ifnormations are available
        data_row = [
            col.text for col in rows[1].find_elements_by_css_selector("td")]
        # list of expected values
        expected_values = [
            '1', "Created", user.username,
            robject.create_date.strftime("%Y-%m-%d, %H:%M"), "—"]
        self.assertSequenceEqual(expected_values, data_row)
