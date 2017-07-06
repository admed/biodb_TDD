from functional_tests.base import FunctionalTest
class UserSignInTests(FunctionalTest):
    def test_user_encounters_login_page(self):
        # User heard about biodb app and decide to visit this website. Received
        # adress leads him to welcome page. Welcome page contains welcome
        # message, login form with two fields and link to sign up form.
        self.browser.get(self.live_server_url)
        self.assertEqual(
        self.browser.current_url, self.live_server_url + "/accounts/login/"
        )
        header = self.browser.find_element_by_id("header")
        description = self.browser.find_element_by_id("description")
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
        form_inputs_id = [input_.get_attribute("id") for input_ in form_inputs]
        for ID in ["login_input", "password_input"]:
            self.assertIn(ID, form_inputs_id)

        link = self.browser.find_element_by_id("sign_up_link")
        self.assertEqual(link.text, "Sign up")

    def test_user_logs_in_without_problems(self):
        pass

    def test_user_encounters_login_form_validation(self):
        pass
