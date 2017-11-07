from django.test import tag
from functional_tests.base import FunctionalTest
from robjects.models import Robject


@tag('slow')
class RobjectHistoryTestCase(FunctionalTest):
    reset_sequences = True

    @property
    def DEFAULT_URL(self):
        return self.live_server_url + reverse("projects:robjects:robject_history",
                                              kwargs={"project_name": "project_1", "robject_id": 1})

    def get_robject_history_url(self, proj, robj):
        """Method returning History url of robject"""
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/{robj.pk}/history/")

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_kwarg_helper(self.ROBJECT_HISTORY_URL)

    def test_annonymous_user_visit_history_page(self):
        self.annonymous_testing_helper(self.ROBJECT_HISTORY_URL)

    def test_user_request_history_page_without_project_visit_permission(self):
        self.permission_view_testing_helper(self.ROBJECT_HISTORY_URL)

    def test_user_visit_history_for_created_robject(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject
        robject = Robject.objects.create(name='robject_1', project=proj,
                                         create_by=user)
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
        header = table.find_element_by_css_selector('thead')
        # the're five columns in table
        header_cols = header.find_elements_by_css_selector("th")
        self.assertEqual(len(header_cols), 5)
        # user checking the columns names
        expected_table_heders = ["Version", "Type",	"Changed by",
                                 "Modyfication date", "Changes"]
        table_headers = [col.text for col in header_cols]
        self.assertSequenceEqual(expected_table_heders, table_headers)
        # user is looking into table data
        body = table.find_elements_by_css_selector("tbody")
        # checking nuber of table rows
        body_rows = body[0].find_elements_by_css_selector("tr")
        self.assertEqual(len(body_rows), 1)
        # user looking into data, only creation ifnormations are available
        data_row = [
            col.text for col in body_rows[0].find_elements_by_css_selector("td")]
        # list of expected values
        expected_values = [
            '1', "Created", user.username,
            robject.create_date.strftime("%Y-%m-%d, %H:%M"), "—"]
        self.assertSequenceEqual(expected_values, data_row)

    def test_user_visit_history_for_edited_robject__no_changes(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject and save it
        robject = Robject.objects.create(name='robject_1', project=proj,
                                         create_by=user)
        # robject name is edited and saved but non of the fields changed
        robject.modify_by = user
        # save the changes to register history
        robject.save()
        # User visits history page of the robject
        self.get_robject_history_url(proj, robject)
        # user see the table
        table = self.browser.find_element_by_css_selector('table')
        # user is looking into table data
        body = table.find_elements_by_css_selector("tbody")
        # checking nuber of table rows
        body_rows = body[0].find_elements_by_css_selector("tr")
        self.assertEqual(len(body_rows), 2)
        # user looking into data, only creation ifnormations are available
        data_row = [
            col.text for col in body_rows[1].find_elements_by_css_selector("td")]
        # list of expected values
        expected_values = [
            '2', "Changed", user.username,
            robject.modify_date.strftime("%Y-%m-%d, %H:%M"), "—"]
        self.assertSequenceEqual(expected_values, data_row)

    def test_user_visit_history_for_edited_robject__with_one_field_changed(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject
        robject = Robject.objects.create(name='robject_1', project=proj,
                                         create_by=user)
        # robject name is modified
        robject.name = "namechanged"
        robject.modify_by = user
        # save the changes to register history
        robject.save()
        # User visits history page of the robject
        self.get_robject_history_url(proj, robject)
        # user see the table
        table = self.browser.find_element_by_css_selector('table')
        # user is looking into table data
        body = table.find_elements_by_css_selector("tbody")
        # user see the two rows in table
        body_rows = body[0].find_elements_by_css_selector("tr")
        self.assertEqual(len(body_rows), 2)
        # check the data from last row
        data_row = [
            col.text for col in body_rows[1].find_elements_by_css_selector("td")]
        # list of expected values
        expected_values = [
            '2', "Changed", user.username,
            robject.modify_date.strftime("%Y-%m-%d, %H:%M")]
        # assertion for four first columns
        self.assertListEqual(expected_values, data_row[0:4])
        # chceck the data from last column "Changes"
        changes_col = body_rows[1].find_elements_by_css_selector(
            "div.field-diff")
        # data should contains new and old section
        changes_col_html = changes_col[0].get_attribute("outerHTML")
        expeted_html = """<div class="field-diff">name
            <div class="new">namechanged</div>
            <div class="old">robject_1</div>
        </div>"""
        # assert html equals
        self.assertHTMLEqual(expeted_html, changes_col_html)

    def test_user_visit_history_for_edited_robject__many_field_changed(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject
        robject = Robject.objects.create(name='robject_1', project=proj,
                                         create_by=user)
        # robject fields (10) are changed
        robject.name = "newname"
        robject.notes = "newnotes"
        robject.ref_seq = "newrefseq"
        robject.mod_seq = "newmodseq"
        robject.description = "newdescription"
        robject.bibliography = "newbibliography"
        robject.ref_commercial = "newrefcommercial"
        robject.ref_clinical = "newrefclinical"
        robject.ligand = "newligand"
        robject.receptor = "newreceptor"
        # set the user who making changes
        robject.modify_by = user
        # save the changes to register history
        robject.save()
        # User visits history page of the robject
        self.get_robject_history_url(proj, robject)
        # user see the table
        table = self.browser.find_element_by_css_selector('table')
        # user is looking into table data
        body = table.find_elements_by_css_selector("tbody")
        # user see the two rows in table
        body_rows = body[0].find_elements_by_css_selector("tr")
        self.assertEqual(len(body_rows), 2)
        # check the data from last row
        data_row = [
            col.text for col in body_rows[1].find_elements_by_css_selector("td")]
        # list of expected values
        expected_values = [
            '2', "Changed", user.username,
            robject.modify_date.strftime("%Y-%m-%d, %H:%M")]
        # assertion for four first columns
        self.assertListEqual(expected_values, data_row[0:4])
        # chceck the data from last 5th column "Changes"
        changes_col = body_rows[1].find_elements_by_css_selector(
            "div.field-diff")
        # check the number of divs
        self.assertEqual(len(changes_col), 10)


def test_user_visit_history_for_edited_robject__multiple_editions(self):
    # login a user and create a project
    user, proj = self.project_set_up_using_default_data(
        permission_visit=True)
    # create an robject
    robject = Robject.objects.create(name='robject_1', project=proj,
                                     create_by=user)
    # robject edited multiple times
    # first
    robject.name = "newname1"
    robject.modify_by = user
    robject.save()
    # second
    robject.name = "newname2"
    robject.modify_by = user
    robject.save()
    # third
    robject.name = "newname3"
    robject.modify_by = user
    robject.save()
    # User visits history page of the robject
    self.get_robject_history_url(proj, robject)
    # user see the table
    table = self.browser.find_element_by_css_selector('table')
    # user is looking into table data
    body = table.find_elements_by_css_selector("tbody")
    # user see 4 rows in the table
    body_rows = body[0].find_elements_by_css_selector("tr")
    self.assertEqual(len(body_rows), 4)
    # each row has information about chages in last column
    changes_cols = body_rows[1].find_elements_by_css_selector("div.field-diff")
    # check the number of divs
    self.assertEqual(len(changes_cols), 4)
