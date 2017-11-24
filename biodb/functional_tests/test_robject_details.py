from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Robject
from guardian.shortcuts import assign_perm


@tag('slow')
class TestUserVisitsRobjectDetails(FunctionalTest):

    def create_data(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        # CREATE SAMPLE SAMPLE FOR PROJECT.
        return(usr, proj, robj)

    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_slug_helper(self.ROBJECT_DETAILS_URL)

    def test_annonymous_user_visits_details(self):
        # CREATE A PROJECT BASIC INFORMATIONS.
        proj = Project.objects.create(name="project_1")
        # CREATE A ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj)
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/{robj.id}/details/")
        current_url = self.browser.current_url
        # Annonymus user is redirected to login page.
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/robjects/{robj.id}/details/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_permission_wants_to_vist_sample_detail_page(self):
        self.permission_view_testing_helper(self.ROBJECT_DETAILS_URL)

    def test_user_with_permission_visit_details_and_checks_static_elements(self):
        # CREATE INITIAL DATA.
        usr, proj, robj = self.create_data()
        # ASSIGN PERMISSIONS FOR PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)

        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/{robj.id}/details/")
        # User seas header which is sample code.
        header_content = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header_content.text, "robject_1")
        # User also seas return to samples table link.
        link = self.browser.find_element_by_css_selector("a.link_back")
        self.assertEqual(link.text, "Back to robject table")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + f"/projects/{proj.name}/robjects/")

    def test_user_checks_robject_details_on_page(self):
        # CREATE SAMPLE USER AND PROJECT.
        usr, proj = self.project_set_up_using_default_data()
        # SET USER PERMISSION FOR PROJECT.
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE SAMPLE ROBJECT.
        robj = Robject.objects.create(name='robject_1', project=proj,
                                      author=usr, create_by=usr,
                                      notes="Test Note",
                                      ref_seq="AAGGMTYWRALKTP",
                                      mod_seq="MILA",
                                      description="Some description",
                                      bibliography="1. A, 2. B",
                                      ref_commercial="ALAMAKITI",
                                      ref_clinical="None",
                                      ligand="Viagra",
                                      receptor="Protein")

        # User want to visit robject detail page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/{robj.id}/details/")

        # User checks list of general fields
        general_fields = self.browser.find_element_by_class_name(
            "general-fields")

        self.assertIn(
            f"ID: {robj.pk}", general_fields.text)
        self.assertIn(
            f"author: {robj.author}", general_fields.text)
        self.assertIn(
            f"create by: {robj.create_by}", general_fields.text)
        self.assertIn(
            f"modify by: None", general_fields.text)
        # User checks list of detail fields
        details_fields = self.browser.find_element_by_class_name(
            "details-fields")
        # User checs all detail fields he set into robject
        for field, field_value in robj.get_detail_fields():
            self.assertIn(
                f"{field}: {field_value}", details_fields.text)
