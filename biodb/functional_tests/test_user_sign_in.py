from functional_tests.base import FunctionalTest
from django.contrib.auth.models import User
class UserSignInTests(FunctionalTest):
    def test_user_encounters_login_page(self):
        # User heard about biodb app and decide to visit this website. Received
        # adress leads him to welcome page. Welcome page contains welcome
        # message, login form with two fields and submit button and link to sign
        # up form.
        self.browser.get(self.live_server_url)
        self.assertEqual(
            self.browser.current_url, self.live_server_url + "/accounts/login/"
        )
        header = self.browser.find_element_by_id("header")
        description = self.browser.find_element_by_id("description")
        submit_button = self.browser.find_element_by_id("submit_button")
        self.assertEqual(
        header.text,
        "Welcome to BioDB"
        )
        self.assertEqual(
        description.text,
        "App that helps you manage your biological research"
        )
        login_form = self.browser.find_element_by_id("login_form")
        form_inputs = login_form.find_elements_by_tag_name("input")
        submit_button = self.browser.find_element_by_id("submit_button")
        form_inputs_id = [input_.get_attribute("id") for input_ in form_inputs]

        for ID in ["login_input", "password_input"]:
            self.assertIn(ID, form_inputs_id)
        self.assertEqual(submit_button.text, "Sign up")

        link = self.browser.find_element_by_id("sign_up_link")

        self.assertEqual(link.text, "Sign up")

    def test_user_logs_in_without_problems(self):
        user = User.objects.create_user(
                               username="VitoCorleone", password="cosa_nostra")
        login_input = self.browser.find_element_by_id("login_input")
        password_input = self.browser.find_element_by_id("password_input")
        submit_button = self.browser.find_element_by_id("submit_button")

        login_input.send_keys("VitoCorleone")
        password_input.send_keys("cosa_nostra")
        submit_button.click()

        self.assertEqual(self.browser.current_url, "/projects/")

    def test_user_encounters_login_form_validation(self):
        pass
