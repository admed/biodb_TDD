from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Robject
from django.contrib.auth.models import User
import time
from guardian.shortcuts import assign_perm
from selenium.common.exceptions import NoSuchElementException


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

    def test_annonymous_user_goes_to_confirmation_page(self):
        self.annonymous_testing_helper(
            self.ROBJECT_DELETE_URL, self.ROBJECT_LIST_URL)

    def test_user_without_delete_permission_goes_to_confirmation_page(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        robj = Robject.objects.create(project=proj, name="sample_robj")

        # User goes to 'sample_robj' delete confirmation page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/delete/?{robj.name}={robj.id}")

        # He gets permission denied message.
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(
            error.text, "User doesn't have permission to delete robjects in this project.")

    def test_user_can_delete_single_robject(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj = Robject.objects.create(project=proj, name="sample_robj")

        # User goes to robject list page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")
        # He marks one robject in table and clicks delete button.
        self.browser.find_element_by_css_selector(
            f".row.{robj.name} .checkbox").click()
        self.browser.find_element_by_css_selector(f"#delete-form .delete-button").click()

        # User is redirect to robject delete confirmation page. He sees GET data
        # in url that following the format ?<robject-name>=<robject-id>.
        self.assertEqual(
            self.browser.current_url,
            self.ROBJECT_DELETE_URL + f"?{robj.name}={robj.id}"
        )

        # User sees page with confirmation message, confirm button and
        # 'get back' link.
        confirmation_message = self.browser.find_element_by_css_selector(
            ".message")
        self.assertEqual(
            confirmation_message.text,
            f"Are you sure you want to delete following robject(s): {robj.name} ?"
        )
        confirm_button = self.browser.find_element_by_css_selector(
            ".confirm-delete")
        self.assertEqual(confirm_button.get_attribute("value"), "Confirm")
        link = self.browser.find_element_by_css_selector(".get-back-link")
        self.assertEqual(link.text, "Back to robjects list.")

        # He clicks confirm button and gets back to robject list page.
        confirm_button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/robjects/")

        # He doesn't see now robject row in table.
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_css_selector(f".row .{robj.name}")

    def test_user_try_to_delete_multiple_objects(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj_1 = Robject.objects.create(project=proj, name="sample_robj_1")
        robj_2 = Robject.objects.create(project=proj, name="sample_robj_2")

        # User goes to robject page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")
        # He sees two robjects in table and marks them, then he clicks delete
        # button.
        rows = self.browser.find_elements_by_css_selector(".row")
        self.assertEqual(len(rows), 2)
        for row in rows:
            row.find_element_by_css_selector(".checkbox").click()
        self.browser.find_element_by_css_selector(".delete-button").click()

        # User see appriopriate message and clicks confirmation button.
        confirmation_message = self.browser.find_element_by_css_selector(
            ".message")
        self.assertEqual(
            confirmation_message.text,
            f"Are you sure you want to delete following robject(s): {robj_1.name}, {robj_2.name} ?"
        )
        self.browser.find_element_by_css_selector(".confirm-delete").click()

        # He is redirected to robject list page and he sees no robjects in table.
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/robjects/")
        rows = self.browser.find_elements_by_css_selector(".row")
        self.assertEqual(len(rows), 0)

    def test_user_clicks_delete_button_without_select_any_robjects(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj_1 = Robject.objects.create(project=proj, name="robj_1")
        robj_2 = Robject.objects.create(project=proj, name="robj_2")

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User confirms that any robject row isnt selected.
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 0)

        # He clicks delete button and gets redirect to robjects delete
        # confirmation page. However instead of confirmation message he sees
        # msg informing that he hasn't choose any robject to delete.
        self.browser.find_element_by_css_selector(".delete-button").click()
        self.assertEqual(self.browser.current_url,
                         self.ROBJECT_DELETE_URL + "?")
        msg = self.browser.find_element_by_css_selector(
            ".message")
        self.assertEqual(
            msg.text,
            "You haven't choose any elements to delete. Please, step back and select elements from table."
        )

    def test_user_select_all_rows_when_none_is_selected(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj_1 = Robject.objects.create(project=proj, name="robj_1")
        robj_2 = Robject.objects.create(project=proj, name="robj_2")
        robj_3 = Robject.objects.create(project=proj, name="robj_3")

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User confirms that any robject row isnt selected.
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 0)

        # He clicks select-all checkbox and sees that every checkbox is selected.
        self.browser.find_element_by_css_selector(".select-all").click()
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 3)

        # He clicks select-all checkbox again and sees that none checkbox is
        # selected.
        self.browser.find_element_by_css_selector(".select-all").click()
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 0)

    def test_user_select_all_when_some_rows_are_selected(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj_1 = Robject.objects.create(project=proj, name="robj_1")
        robj_2 = Robject.objects.create(project=proj, name="robj_2")
        robj_3 = Robject.objects.create(project=proj, name="robj_3")

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # He select one row.
        self.browser.find_element_by_css_selector(".robj_1 .checkbox").click()
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 1)

        # Now, he clicks select-all checkbox and confirms that all checkboxes
        # are selected
        self.browser.find_element_by_css_selector(".select-all").click()
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 3)

        # He clicks select-all checkbox again and sees that none checkbox is
        # selected.
        self.browser.find_element_by_css_selector(".select-all").click()
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(".checkbox:checked")), 0)

    def test_user_wants_to_delete_robjects_but_resign_before_confirm(self):
        # SET UP
        proj, user = self.set_up_robject_list()
        assign_perm("can_delete_robjects", user, proj)
        robj_1 = Robject.objects.create(project=proj, name="robj_1")

        # User gets to robj_1 delete confirmation page.
        self.browser.get(self.ROBJECT_DELETE_URL + "?robj_1=1")
        # Instead of confirm deletion he decides to click 'get back link'.
        self.browser.find_element_by_css_selector(".get-back-link").click()
        # He was redirect to robject list page.
        self.assertEqual(self.browser.current_url, self.ROBJECT_LIST_URL)
