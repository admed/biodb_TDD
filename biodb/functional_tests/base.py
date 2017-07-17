import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from django.contrib.auth.models import User
class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 10
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def login_user(self, username, password):
        """ Helper method for log user in.
        """
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_css_selector(
                                                              "#username_input")
        password_input = self.browser.find_element_by_css_selector(
                                                              "#password_input")
        submit_button = self.browser.find_element_by_id("submit_button")

        username_input.send_keys(username)
        password_input.send_keys(password)
        submit_button.click()
        expected_url = self.live_server_url + "/projects/"
        assert self.browser.current_url == expected_url, "User login failed!"
