from functional_tests.base import FunctionalTest
from django.test import tag
from robjects.models import Robject
from projects.models import Project
from django.contrib.auth.models import User
import time
from selenium.common.exceptions import NoSuchElementException


class SearchEngineTests(FunctionalTest):
    DEFAULT_AUTHOR_USERNAME = "AUTHOR"

    @tag('slow')
    def __init__(self, *args, **kwargs):
        super(SearchEngineTests, self).__init__(*args, **kwargs)

        self.search_input = lambda: self.browser.find_element_by_id(
            "search_input")
        self.search_button = lambda: self.browser.find_element_by_id(
            "search_button")

    @tag('slow')
    def send_query(self, query):
        self.search_input().send_keys(query)
        self.search_button().click()

    @tag('slow')
    def look_for_robject_row(self, css):
        self.browser.find_element_by_css_selector(css)

    @tag('slow')
    def create_sample_robject_and_go_to_robjects_page(self,
                                                      project,
                                                      **robject_kwargs):
        # Create sample robject.
        robj = Robject.objects.create(project=project, **robject_kwargs)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{project.name}/robjects/")
        return robj

    @tag('slow')
    def create_sample_robject_then_search_for_him_using_query(self, query,
                                                              robject_kwargs):
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robject.
        # User goes to robjects page.
        robj = self.create_sample_robject_and_go_to_robjects_page(
            project=proj, **robject_kwargs)

        # He sees sample robject in table.
        self.look_for_robject_row(f".row.{robj.name}")

        # User perform search using given query.
        self.send_query(query)

        # And confirm search success.
        self.look_for_robject_row(f".row.{robj.name}")

    @tag('slow')
    def search_for_robject_using_author_query(self, author_query):
        # create default author
        author = User.objects.create_user(
            username=self.DEFAULT_AUTHOR_USERNAME)
        # create sample robject and bond author with it
        self.create_sample_robject_then_search_for_him_using_query(
            query=author_query,
            robject_kwargs={"author": author, "name": "robject_1"})

    @tag('slow')
    def test_user_without_visit_perm_gets_search_page(self):
        self.permission_view_testing_helper(self.ROBJECT_SEARCH_URL)

    @tag('slow')
    def test_user_enter_wrong_slug_in_url(self):
        self.not_matching_url_kwarg_helper(self.ROBJECT_SEARCH_URL)

    @tag('slow')
    def test_user_perform_search_based_on_whole_robj_name_and_find_robject(self):
        project, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robjects.
        Robject.objects.create(name="robject_1", project=project, id=1)
        Robject.objects.create(name="robject_2", project=project, id=2)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         "/projects/project_1/robjects/")

        # He sees two robjects in table.
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(".row.robject_1"))
        self.browser.find_element_by_css_selector(".row.robject_2")

        # User wants to test search tool. He looks for search form.
        search_form = self.browser.find_element_by_id("search_form")

        # User enter name of one robject and expect to see only this robject in
        # table.
        self.search_input().send_keys("robject_1")
        self.search_button().click()

        rows = self.browser.find_elements_by_css_selector(".row")
        self.assertEqual(len(rows), 1)

        self.browser.find_elements_by_css_selector(".robject_1")

    @tag('slow')
    def test_user_search_for_one_robject_using_name_fragment(self):
        # Default setup for robjects page.
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robjects.
        Robject.objects.create(name="robject_1", project=proj)
        Robject.objects.create(name="robject_2", project=proj)

        # User would like to know if he can get search results using part of
        # robject name. To find out he goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # He sees two robjects in table.
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(".row.robject_1"))
        self.browser.find_element_by_css_selector(".row.robject_2")

        # He wants to search for robject with lower id. User enters part of its
        # name and looks for results.
        self.search_input().send_keys("object_1")
        self.search_button().click()

        rows = self.browser.find_elements_by_css_selector(".row")
        self.assertEqual(len(rows), 1)

        self.browser.find_elements_by_css_selector(".robject_1")

    @tag('slow')
    def test_user_search_for_multiple_robjects_using_name_fragment(self):
        # Make set up for robjects page.
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robjects.
        Robject.objects.create(name="robject_1", project=proj)
        Robject.objects.create(name="robject_2", project=proj)
        Robject.objects.create(name="foo", project=proj)

        # User want to find multiple robjects using common part of robject
        # names. He goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User sees three robjects in table.
        table_rows = self.browser.find_elements_by_class_name("row")
        self.assertEqual(len(table_rows), 3)

        # Then he looks for robjects names cotaining 'robject' part and checks
        # result.
        self.search_input().send_keys("robject")
        self.search_button().click()

        self.browser.find_element_by_class_name("robject_1")
        self.browser.find_element_by_class_name("robject_2")
        table_rows = self.browser.find_elements_by_class_name("row")

        self.assertEqual(len(table_rows), 2)

    @tag('slow')
    def test_annonymous_user_cant_request_search_url(self):
        self.annonymous_testing_helper(self.ROBJECT_SEARCH_URL)

    @tag('slow')
    def test_user_search_for_robject_name_using_case_insensitivity(self):
        # User want to search robject using its name, but he dont know what is
        # exact letter case. He knows that name contains letter with both cases
        # and that searching suppouse to be case insensitve. User decide to use
        # all upper case letters and then all lower case letters and compare
        # results.

        # Make set up for robjects page.
        proj, usr = self.default_set_up_for_visit_robjects_pages()

        # Create sample robject.
        robj = Robject.objects.create(name="RoBjEcT_1", project=proj)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User enters name using lower case letters.
        self.search_input().send_keys("robject_1")
        self.search_button().click()
        # User looks for results.
        self.browser.find_element_by_css_selector(f".row.{robj.name}")

        # User enters name using upper case letters.
        self.search_input().send_keys("ROBJECT_1")
        self.search_button().click()

        # User looks for results.
        self.browser.find_element_by_css_selector(f".row.{robj.name}")

    @tag('slow')
    def test_user_can_search_robject_using_full_author_username(self):
        # User goes to robjects page where he can see sample robject in table.
        # He search for robject's author full username and looks if robject is
        # still in table.
        self.search_for_robject_using_author_query(
            self.DEFAULT_AUTHOR_USERNAME)

    @tag('slow')
    def test_user_can_search_robjet_using_fragment_of_athor_username(self):
        # User goes to robjects page where he can see sample robject in table.
        # He search for robject's author username fragment and looks if robject
        # is still in table.
        self.search_for_robject_using_author_query(
            self.DEFAULT_AUTHOR_USERNAME[0:-1])

    @tag('slow')
    def test_user_can_search_robject_using_case_insensitive_full_author_username(self):
        # User goes to robjects page where he can see sample robject in table.
        # He search for robject's author username using mixed case letters and
        # looks if robject is still in table.
        self.search_for_robject_using_author_query("aUtHoR")

    @tag('slow')
    def test_user_can_display_all_robjects_leaving_search_input_empty(self):
        # Make set up for robjects page.
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robjects.
        robj_1 = Robject.objects.create(name="robj_1", project=proj)
        robj_2 = Robject.objects.create(name="robj_2", project=proj)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User sees two robjects in table.
        self.look_for_robject_row(f".row.{robj_1.name}")
        self.look_for_robject_row(f".row.{robj_2.name}")

        # He decides to limit table rows to one robject using search tool.
        self.send_query(f"{robj_1.name}")

        # Now, user wants to know what will happend if he perform search
        # without type anything.
        self.send_query("")

        # He sees all robjects in table once again.
        self.look_for_robject_row(f".row.{robj_1.name}")
        self.look_for_robject_row(f".row.{robj_2.name}")

    @tag('slow')
    def test_user_cant_search_robjects_from_outside_project(self):
        # Make set up for robjects page.
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create new project and attach robject to it.
        other_proj = Project.objects.create(name="other_proj")
        searched_robj = Robject.objects.create(
            name="searched_robj", project=other_proj)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # He wants to know if there is a way to search robject from outside the
        # project. He know about some robject from other project and decide to
        # search it.
        self.send_query(f"{searched_robj.name}")
        # He confirms that there is no required robject in table.
        with self.assertRaises(NoSuchElementException):
            self.look_for_robject_row(f".row.{searched_robj.name}")

    @tag('slow')
    def test_user_can_search_with_many_words(self):
        # Make set up for robjects page.
        proj, user = self.default_set_up_for_visit_robjects_pages()

        # Create sample robjects.
        robj_1 = Robject.objects.create(
            name="robj_1", project=proj, create_by=user)
        robj_2 = Robject.objects.create(
            name="robj_2", project=proj, create_by=user)
        robj_3 = Robject.objects.create(
            name="robj_3", project=proj, create_by=user)

        # User goes to robjects page.
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/robjects/")

        # User sees three robjects in table.
        table_rows = self.browser.find_elements_by_class_name("row")
        self.assertEqual(len(table_rows), 3)

        # He wants to know if there is a way to search two robjects from the
        # project. He want to search two different names and get as result the
        # two robjects.
        self.search_input().send_keys("robj_1 robj_2")
        self.search_button().click()

        self.browser.find_element_by_class_name("robj_1")
        self.browser.find_element_by_class_name("robj_2")
        table_rows = self.browser.find_elements_by_class_name("row")

        self.assertEqual(len(table_rows), 2)

    @tag('slow')
    def test_user_limits_number_of_fields_to_search(self):
        pass

    @tag('slow')
    def test_user_narrows_the_search_to_the_date_range(self):
        pass
