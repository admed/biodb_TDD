from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from functional_tests.base import FunctionalTest
from django.contrib.auth.models import User

class UserLogoutTests(FunctionalTest):
    def test_logged_user_logs_out(self):
        ## Create active user.

        u = User.objects.create_user(username="USERNAME", password="PASSWORD")

        ## Login active user.

        self.login_user(username="USERNAME", password="PASSWORD")

        # User gets to projects page. He wants to logout. He
        # clicks to logout button and is redirected to login page.

        self.browser.get(self.live_server_url + "/projects/")
        logout_button = self.browser.find_element_by_id("logout_button")
        logout_button.click()

        self.assertEqual(self.browser.current_url, self.live_server_url + "/accounts/login/")

        # When he wants to get to projects page he sees permission denied
        # message.

        self.browser.get(self.live_server_url + "/projects/")
        body_element = self.browser.find_element_by_tag_name("body")
        self.assertEqual(body_element.text, "403 Forbidden")

    def test_annonymous_user_cant_find_logout_button(self):
        pass

    def test_annonymous_user_cant_get_to_logut_url(self):
        pass
