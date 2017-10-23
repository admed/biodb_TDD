import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from robjects.models import Robject
from samples.models import Sample
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm


class TestUserVisitsSampleList(FunctionalTest):
    def get_sample_list(self, proj):
        sample_list_url = f"/projects/{proj.name}/samples/"
        response = self.browser.get(self.live_server_url + sample_list_url)
        return response

    def get_rows_from_table(self):
        table = self.browser.find_element_by_css_selector('table')
        rows = table.find_elements_by_css_selector(".row.sample")
        return rows

    def assert_cells_content_in_row(self, proj, sample):
        table = self.browser.find_element_by_css_selector('table')
        rows = table.find_elements_by_css_selector(".row.sample")
        self.assertEqual(len(rows), 1)
        # He looks for data in every cell in row and copare it with sample data.
        cells = rows[0].find_elements_by_css_selector("td")
        self.assertEqual(cells[0].text, str(sample.id))
        self.assertEqual(cells[1].text, sample.code)
        self.assertEqual(cells[2].text, sample.robject.name)
        self.assertEqual(cells[3].text, sample.owner.username)
        self.assertEqual(
            cells[4].text, sample.create_date.strftime('%Y-%m-%d, %H:%M'))
        self.assertEqual(
            cells[5].text, sample.modify_date.strftime('%Y-%m-%d, %H:%M'))
        self.assertEqual(cells[6].text, sample.modify_by.username)
        self.assertEqual(cells[7].text, sample.notes)
        self.assertEqual(cells[8].text, sample.form)
        self.assertEqual(cells[9].text, sample.source)
        self.assertEqual(cells[10].text, sample.get_status_display())
        self.assertEqual(
            cells[11].find_element_by_tag_name("a").get_attribute('href'),
            self.live_server_url + f"/projects/{proj.name}/samples/{sample.id}/update/"
        )

    def test_annonymous_user_visits_samples_list(self):
        # Create sample robjects basic informations.
        proj = Project.objects.create(name="project_1")
        # Annonymus user can not visit raport pdf page.
        # uses function from base module
        self.get_sample_list(proj)
        current_url = self.browser.current_url
        expected_url = self.live_server_url + \
            f"/accounts/login/?next=/projects/{proj.name}/samples/"
        self.assertEqual(current_url, expected_url)

    def test_user_without_project_visit_permission_tries_to_get_sample_list(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()

        # User gets sample list. He doesn't have project visit permission.
        self.get_sample_list(proj)
        # He sees perrmision denied error.
        error = self.browser.find_element_by_css_selector("h1")
        self.assertEqual(error.text, "403 Forbidden")

    def test_user_discovers_table_and_previous_page_link(self):
        # CREATE SAMPLE PROJECT AND USER
        usr, proj = self.project_set_up_using_default_data()
        # ASSIGN PERMISSION TO PROJECT
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets sample list.
        self.get_sample_list(proj)
        # He sees table with header that contains following column names
        # with order: Id, Code, Robject, Owner, Create date, Modify date,
        # Modify by, Notes, Form, Source, Status, Edit Entries
        table = self.browser.find_element_by_css_selector('table')
        headers = table.find_elements_by_css_selector('th')
        header_names = ["Id", "Code", "Robject", "Owner", "Create date", "Modify date",
                        "Modify by", "Notes", "Form", "Source", "Status", "Edit"]
        self.assertEqual(len(headers), len(header_names))
        for header, expected_header_name in zip(headers, header_names):
            self.assertEqual(header.text, expected_header_name)
        # Finally user clicks link to projects list in the bottom of page.
        link = self.browser.find_element_by_css_selector("a.link_back")
        link.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

    def test_user_examine_one_sample_row(self):
        # CREATE SAMPLE PROJECT AND ROBJECT
        usr, proj = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECT
        robject = Robject.objects.create(name='robject_1', project=proj)
        # CRETE SAMPLE
        sample = Sample.objects.create(
            code='S1',
            robject=robject,
            owner=usr,
            modify_by=usr,
            notes="top secret",
            form="solid",
            source="budynek E, pokój 13",
            status=10
        )
        # ASSIGN PERMISSION TO USER
        assign_perm("projects.can_visit_project", usr, proj)
        # User gets sample list.
        self.get_sample_list(proj)
        # He sees table and single row.
        rows = self.get_rows_from_table()
        self.assertEqual(len(rows), 1)
        # He looks for data in every cell in row and copare it with sample data.
        self.assert_cells_content_in_row(proj, sample)

    def test_user_examine_another_one_sample_row(self):
        # CREATE SAMPLE USER
        usr = self.login_user(username='Justin Bieber', password='ILoveJB')
        # CREATE SAMPLE PROJECT
        proj = Project.objects.create(name='Project_1')
        # ASSIGN PERMISSION TO USER
        assign_perm("projects.can_visit_project", usr, proj)
        # CREATE SAMPLE ROBJECT
        robject = Robject.objects.create(name='robject_2', project=proj)
        # CREATE SAMPLE
        sample = Sample.objects.create(
            code='S2',
            robject=robject,
            owner=usr,
            modify_by=usr,
            notes="not secret",
            form="liquid",
            source="budynek A, pokój 245",
            status=1
        )
        # User gets sample list.
        self.get_sample_list(proj)
        # He sees table and single row.
        rows = self.get_rows_from_table()
        self.assertEqual(len(rows), 1)
        # He looks for data in every cell in row and copare it with sample data.
        self.assert_cells_content_in_row(proj, sample)

    def test_user_sees_multiple_samples_in_table_for_certain_project(self):
        # CREATE SAMPLE PROJECT AND ROBJECT
        usr, proj1 = self.project_set_up_using_default_data()
        # CREATE EXTRA PROJECT
        proj2 = Project.objects.create(name="project_2")
        # CREATE SAMPLE ROBJECTS
        robject_1 = Robject.objects.create(name='robject_1', project=proj1)
        robject_2 = Robject.objects.create(name='robject_2', project=proj2)
        # CRETE SAMPLE SAMPLES
        sampl1 = Sample.objects.create(code='Sample1', robject=robject_1)
        sampl2 = Sample.objects.create(code="Sample2", robject=robject_2)
        sampl3 = Sample.objects.create(code="Sample3", robject=robject_1)
        sampl4 = Sample.objects.create(code="Sample4", robject=robject_2)

        # ASSIGN PERMISSION TO USER
        assign_perm("projects.can_visit_project", usr, proj1)
        # User gets sample list.
        self.get_sample_list(proj1)
        # User know that there is two samples for one project and two samples for other.
        # He checks that table contains appropiate samples for current project.
        rows = self.get_rows_from_table()
        self.assertEqual(len(rows), 2)

    def test_user_clicks_sample_code_link_and_seas_sample_details(self):
        # CREATE SAMPLE PROJECT AND ROBJECT
        usr, proj1 = self.project_set_up_using_default_data()
        # CREATE SAMPLE ROBJECTS
        robject_1 = Robject.objects.create(name='robject_1', project=proj1)
        # CRETE SAMPLE SAMPLE.
        sample = Sample.objects.create(code='Sample1',
                                       robject=robject_1,
                                       owner=usr,
                                       modify_by=usr,
                                       notes="Notes")
        # ASSIGN PERMISSION TO USER
        assign_perm("projects.can_visit_project", usr, proj1)
        # User gets sample list.
        response = self.get_sample_list(proj1)
        # User clicks on sample_code.
        link = self.browser.find_element_by_css_selector("a.sample-details")
        link.click()
        # User seas sample details informations.
        detail_list = self.browser.find_elements_by_css_selector("li")

        self.assertIn(sample.robject.name, detail_list[0].text)
        self.assertIn(sample.owner.username, detail_list[1].text)
        self.assertIn(sample.create_date.strftime(
            '%Y-%m-%d, %H:%M'), detail_list[2].text)
        self.assertIn(sample.modify_date.strftime(
            '%Y-%m-%d, %H:%M'), detail_list[3].text)
        self.assertIn(sample.modify_by.username, detail_list[4].text)
        self.assertIn(sample.notes, detail_list[5].text)
        self.assertIn(sample.form, detail_list[6].text)
        self.assertIn(sample.source, detail_list[7].text)
        self.assertIn(sample.get_status_display(), detail_list[8].text)
