import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from projects.models import Project


class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.main_window = None
        while not self.main_window:
            self.main_window = self.browser.current_window_handle

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

    def get_popup_window(self):
        popup_window = None
        while not popup_window:
            for handle in self.browser.window_handles:
                if handle != self.main_window:
                    popup_window = handle
                    break
        return popup_window

    def switch_to_popup(self):
        popup_window = self.get_popup_window()
        self.browser.switch_to.window(popup_window)

    def switch_to_main(self):
        self.browser.switch_to.window(self.main_window)

    def login_user(self, username, password):
        """ Helper method for log user in.
        """
        try:
            u = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            u = User.objects.get(username=username)
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
        assert self.browser.current_url == expected_url, f"User login failed!"

        return u

    def project_set_up_using_default_data(self):
        """ Helper method for all robject page related tests.
            Method include logged user with default creadentials and project
            with default name.
        """
        user = self.login_user("USERNAME", "PASSWORD")

        proj = Project.objects.create(name="project_1")

        self.browser.get(self.live_server_url + f"/projects/{proj}/robjects/")

        return user, proj
