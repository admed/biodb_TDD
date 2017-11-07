from functional_tests.base import FunctionalTest
from guardian.shortcuts import assign_perm
from django.core.urlresolvers import reverse
from projects.models import Project
from robjects.models import Robject, Name, Tag
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
import time
from django.utils import timezone
from selenium.webdriver.common.keys import Keys


class RobjectEditView(FunctionalTest):

    def set_up_robject_edit(self):
        self.DEFAULT_PROJECT = Project.objects.create(name="project_1")
        self.DEFAULT_USER = User.objects.create_user(
            username="USERNAME", password="PASSWORD")
        self.DEFAULT_NAME = Name.objects.create(name="DEFAULT_NAME")
        self.DEFAULT_TAG = Tag.objects.create(name="DEFAULT_TAG")
        self.DEFAULT_ROBJECT = Robject.objects.create(
            project=self.DEFAULT_PROJECT,
            author=self.DEFAULT_USER,
            name="DEFAULT_NAME",
            create_by=self.DEFAULT_USER,
            modify_by=self.DEFAULT_USER,
            notes="DEFAULT_NOTES",
            ref_seq="DEFAULT_REF_SEQ",
            mod_seq="DEFAULT_MOD_SEQ",
            description="DEFAULT_DESCRIPTION",
            bibliography="DEFAULT_BIBLIOGRAPHY",
            ref_commercial="DEFAULT_REF_COMMERCIAL",
            ref_clinical="DEFAULT_REF_CLINICAL",
            ligand="DEFAULT_LIGAND",
            receptor="DEFAULT_RECEPTOR",
        )
        self.DEFAULT_ROBJECT.names.add(self.DEFAULT_NAME)
        self.DEFAULT_ROBJECT.tags.add(self.DEFAULT_TAG)
        self.DEFAULT_ROBJECT.save()

        self.login_user("USERNAME", "PASSWORD")
        assign_perm("can_visit_project", self.DEFAULT_USER,
                    self.DEFAULT_PROJECT)
        assign_perm("can_modify_project",
                    self.DEFAULT_USER, self.DEFAULT_PROJECT)

    def get_page(self):
        url = reverse("projects:robjects:robject_edit", kwargs={
            "project_name": self.DEFAULT_PROJECT.name,
            "robject_id": self.DEFAULT_ROBJECT.id
        })
        self.browser.get(self.live_server_url + url)

    def add_related_name(self, name):
        """User click in plus button, switch to popup, add related and get back.
        """
        plus_btn = self.browser.find_element_by_css_selector(
            f".related-widget-wrapper select#id_names + a")
        plus_btn.click()

        self.switch_to_popup()
        name_input = self.browser.find_element_by_css_selector(
            "input[name='name']")
        name_input.send_keys(name)
        self.browser.find_element_by_css_selector(
            "input[type='submit']").click()
        self.switch_to_main()

    def add_related_tag(self, name):
        """ User click in plus button, switch to popup, add related and get back.
        """
        plus_btn = self.browser.find_element_by_css_selector(
            f".related-widget-wrapper select#id_tags + a")
        plus_btn.click()

        self.switch_to_popup()
        name_input = self.browser.find_element_by_css_selector(
            "input[name='name']")
        name_input.send_keys(name)
        self.browser.find_element_by_css_selector(
            "input[type='submit']").click()
        self.switch_to_main()

    def confirm_names_input(self, name):
        option_tag = self.wait_for(lambda: self.browser.find_element_by_css_selector(
            f".related-widget-wrapper select#id_names option:last-child"))

        self.assertEqual(option_tag.text, name)

    def confirm_tags_input(self, name):
        option_tag = self.wait_for(lambda: self.browser.find_element_by_css_selector(
            f".related-widget-wrapper select#id_tags option:last-child"))

        self.assertEqual(option_tag.text, name)

    def confirm_text_input(self, field_name, text):
        field = self.browser.find_element_by_css_selector("#id_" + field_name)
        self.assertEqual(field.get_attribute("value"), text)

    def confirm_CKE_input(self, field_name, text):
        frame = self.browser.find_element_by_css_selector(
            f"#cke_id_{field_name} iframe")
        self.browser.switch_to_frame(frame)
        field = self.browser.find_element_by_tag_name("body")
        self.assertEqual(field.text, text)
        self.switch_to_main()

    def confirm_author_input(self, username):
        author_option = self.browser.find_element_by_xpath(
            f"//option[contains(text(), '{username}')]")
        self.assertEqual(author_option.get_attribute("selected"), "true")

    def submit_form(self):
        self.browser.find_element_by_css_selector("button").click()

    def validate_redirection(self):
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url +
            reverse("projects:robjects:robjects_list",
                    kwargs={"project_name": self.DEFAULT_PROJECT.name})
        )

    def fill_CKE_field(self, field_name, text):
        """ User add some text to cke field.
        """
        frame = self.browser.find_element_by_css_selector(
            f"#cke_id_{field_name} iframe")
        self.browser.switch_to_frame(frame)
        field = self.browser.find_element_by_tag_name("body")
        field.clear()
        field.send_keys(text)
        self.switch_to_main()

    def fill_text_field(self, field_name, text):
        field = self.browser.find_element_by_css_selector("#id_" + field_name)
        field.clear()
        field.send_keys(text)

    def choose_author(self, username):
        author_option = self.browser.find_element_by_xpath(
            f"//option[contains(text(), '{username}')]")
        author_option.click()

    def confirm_robject_fields(self, data, names=[], tags=[]):
        r = Robject.objects.last()
        for key, value in data.items():
            self.assertEqual(getattr(r, key), value)

        robject_names = [name.name for name in r.names.all()]
        for name in names:
            self.assertIn(name, robject_names)

        robject_tags = [tag.name for tag in r.tags.all()]
        for tag in tags:
            self.assertIn(tag, robject_tags)

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_kwarg_helper(self.ROBJECT_EDIT_URL)

    def test_annonymous_user_goes_to_confirmation_page(self):
        self.annonymous_testing_helper(self.ROBJECT_EDIT_URL)

    def test_user_sees_filled_fields_inside_form(self):
        self.set_up_robject_edit()
        self.get_page()
        self.confirm_author_input("USERNAME")
        self.confirm_text_input("name", "DEFAULT_NAME")
        self.confirm_text_input("ligand", "DEFAULT_LIGAND")
        self.confirm_text_input("receptor", "DEFAULT_RECEPTOR")
        self.confirm_CKE_input("notes", "DEFAULT_NOTES")
        self.confirm_CKE_input("ref_seq", "DEFAULT_REF_SEQ")
        self.confirm_CKE_input("mod_seq", "DEFAULT_MOD_SEQ")
        self.confirm_CKE_input("description", "DEFAULT_DESCRIPTION")
        self.confirm_CKE_input("bibliography", "DEFAULT_BIBLIOGRAPHY")
        self.confirm_CKE_input("ref_commercial", "DEFAULT_REF_COMMERCIAL")
        self.confirm_CKE_input("ref_clinical", "DEFAULT_REF_CLINICAL")
        self.confirm_names_input("DEFAULT_NAME")
        self.confirm_tags_input("DEFAULT_TAG")

    def test_user_modify_all_fields(self):
        self.set_up_robject_edit()
        self.get_page()
        self.fill_text_field("name", "new_name")
        self.fill_text_field("ligand", "new_ligand")
        self.fill_text_field("receptor", "new_receptor")
        self.fill_CKE_field("notes", "new_notes")
        self.fill_CKE_field("ref_seq", "new_ref_seq")
        self.fill_CKE_field("mod_seq", "new_mod_seq")
        self.fill_CKE_field("description", "new_description")
        self.fill_CKE_field("bibliography", "new_bibliography")
        self.fill_CKE_field("ref_commercial", "new_ref_commercial")
        self.fill_CKE_field("ref_clinical", "new_ref_clinical")
        self.add_related_name("new_name")
        self.add_related_tag("new_tag")
        self.submit_form()
        data = {
            "name": "new_name",
            "ligand": "new_ligand",
            "receptor": "new_receptor",
            "notes": "<p>new_notes</p>",
            "ref_seq": "<p>new_ref_seq</p>",
            "mod_seq": "<p>new_mod_seq</p>",
            "description": "<p>new_description</p>",
            "bibliography": "<p>new_bibliography</p>",
            "ref_commercial": "<p>new_ref_commercial</p>",
            "ref_clinical": "<p>new_ref_clinical</p>"
        }
        self.confirm_robject_fields(data, names=[
                                    "new_name"], tags=["new_tag"])

    def test_different_user_edit_robject(self):
        self.set_up_robject_edit()
        u = self.login_user("NEW_USERNAME", "NEW_PASSWORD")
        assign_perm("can_visit_project", u, self.DEFAULT_PROJECT)
        assign_perm("can_modify_project", u, self.DEFAULT_PROJECT)
        self.get_page()
        self.fill_text_field("name", "new_name")
        self.submit_form()
        r = Robject.objects.last()
        self.assertEqual(r.modify_by.username, "NEW_USERNAME")

    def test_user_is_redirect_to_robject_list(self):
        self.set_up_robject_edit()
        self.get_page()
        self.fill_text_field("name", "new_name")
        self.submit_form()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + reverse("projects:robjects:robjects_list",
                                           kwargs={"project_name": self.DEFAULT_PROJECT.name})
        )
