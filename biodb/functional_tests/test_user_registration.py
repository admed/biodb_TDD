from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from functional_tests.base import FunctionalTest
from django.contrib.auth.models import User

class UserRegistrationTests(FunctionalTest):
    def setUp(self):
        super(UserRegistrationTests, self).setUp()
        sign_up_form = lambda: self.browser.find_element_by_id("sign_up_form")
        self.username_input = lambda: sign_up_form().find_element_by_id(
                                                               "username_input")
        self.email_input = lambda: sign_up_form().find_element_by_id(
                                                                  "email_input")
        self.password_input = lambda: sign_up_form().find_element_by_id(
                                                               "password_input")
        self.confirm_input = lambda: sign_up_form().find_element_by_id(
                                                                "confirm_input")
        self.submit_button = lambda: sign_up_form().find_element_by_id(
                                                                "submit_button")
    def test_user_use_sign_up_form_without_problems(self):
        # User heard about biodb app and decide to visit this website. Received
        # adress leads him to welcome page. Welcome page contains link to sign
        # up form.
        self.browser.get(self.live_server_url)

        link = self.browser.find_element_by_id("sign_up_link")

        # Excited user clicks sign up link. Current relative url is:
        # '/accounts/sing-up/'.
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/sign-up/"
        )

        # User noticed new form with several fields: username, email adress,
        # password and repeat password and submit button. Each has its own
        # placeholder.

        self.assertEqual(
        self.username_input().get_attribute("placeholder"),
        "username"
        )
        self.assertEqual(
        self.email_input().get_attribute("placeholder"),
        "email"
        )
        self.assertEqual(
        self.password_input().get_attribute("placeholder"),
        "password"
        )
        self.assertEqual(
        self.confirm_input().get_attribute("placeholder"),
        "confirm password"
        )
        self.assertEqual(self.submit_button().text, "Submit")

        # Passwords fields are of type "password".
        self.assertEqual(
                        self.password_input().get_attribute("type"), "password")
        self.assertEqual(self.confirm_input().get_attribute("type"), "password")

        # User is first user ever who sign-up to BioDB. He fills form with data
        # and click submit.
        credentials = {
            "username": "John Lenon",
            "email": "john.lennon@beatles.uk",
            "password": "i_m_the_best_beatle_paul",
        }
        self.username_input().send_keys(credentials["username"])
        self.email_input().send_keys(credentials["email"])
        self.password_input().send_keys(credentials["password"])
        self.confirm_input().send_keys(credentials["password"])
        self.submit_button().click()

        # Success! He is redirected to a login page.
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/login/"
        )

    def test_user_encounters_form_validation(self):
        # User goes stright to sign-up form page.
        self.browser.get(self.live_server_url + "/accounts/sign-up/")

        # Curoius user wants to know what will happend when he clicks submit
        # button before fill any field. Instead of redirect he stays in the same
        # page.
        current_url = self.browser.current_url
        self.submit_button().click()
        self.assertEqual(current_url, self.browser.current_url)

        # Now user sees error messages bound to every field.
        for el in ["username", "email", "password", "confirm_password"]:
            self.assertEqual(
                self.browser.find_element_by_id("{}_errorlist".format(el)).text,
                "This field is required."
            )

        # He suspect that form has data duplication validation. His close fellow
        # Bilbo Baggins has account in BioDB and user knows his credentials.
        # First he checks for username. Above form appears following message:
        # 'User with such username or email already exists'.

        ## create user inside DB
        username = "Bilbo"
        email = "bilbo@baggins.shire.mde"
        password = "damn_dragon!"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        ## refresh page to delete previous form errors
        self.browser.get(self.live_server_url + "/accounts/sign-up/")


        self.username_input().send_keys('Bilbo')
        self.submit_button().click()

        error = self.browser.find_element_by_css_selector(
                                                      ".errorlist.nonfield").text

        self.assertEqual(
            error,
            "User with such username or email already exists".format(el)
        )

        # Curoius user decides to check if the same goes for email input. He
        #  User enters Bilbo's email and looks for errors.

        ## refresh page to delete previous form errors
        self.browser.get(self.live_server_url + "/accounts/sign-up/")

        self.email_input().send_keys('bilbo@baggins.shire.mde')
        self.submit_button().click()

        error = self.browser.find_element_by_css_selector(
                                                      ".errorlist.nonfield").text

        self.assertEqual(
            error,
            "User with such username or email already exists"
        )

        # Finally user want to check password validation. He enters different
        # passwords in confirm password field and looks for error.
        self.browser.get(self.live_server_url + "/accounts/sign-up/")

        self.password_input().send_keys("top_secret")
        self.confirm_input().send_keys("less_secret")

        self.submit_button().send_keys(Keys.ENTER)
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                                                     ".errorlist.nonfield").text
        )
        self.assertEqual(error, "Passwords doesn't match.")

        # Ok that works. But user wonders what will happen if he commit two
        # previous validation at once. He fills appropriate fields with data
        # and looks for errors.

        self.browser.get(self.live_server_url + "/accounts/sign-up/")

        self.username_input().send_keys('Bilbo')
        self.password_input().send_keys("top_secret")
        self.confirm_input().send_keys("less_secret")
        self.submit_button().click()

        errors = self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                                                     ".errorlist.nonfield").text
        )
        self.assertIn("Passwords doesn't match.", errors)
        self.assertIn("User with such username or email already exists", errors)
