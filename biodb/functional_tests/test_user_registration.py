from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase

class UserRegistrationTests(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_registration(self):
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


        # Excited user clicks sign up link. Current relative url is:
        # '/accounts/sing-up/'.
        link.click()
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/sign-up/"
        )

        # User noticed new form with several fields: username, email adress,
        # password and repeat password. Each has its own placeholder

        # sign_up_form = self.browser.find_element_by_id("sign_up_form")
        # username_input = sign_up_form.find_element_by_id("username_input")
        # email_input = sign_up_form.find_element_by_id("email_input")
        # password_input = sign_up_form.find_element_by_id("password_input")
        # repeat_input = sign_up_form.find_element_by_id("repeat_input")



        # Distracted user accidentaly clicks submit button before fill any
        # field. Every field is requried so now he sees error messages bound
        # with any field.
        self.fail("Finish test!")

        # Immediately decides to repair his mistake and starts to fill the form
        # with data. But he dont know that user with such username, email and
        # password already exists in database. He quickly learns about it when
        # he clicks submit button. Above every field now appear message with
        # appropriate message: 'user with such <field> already exists'.

        # User fills form with new data and clicks submit button once again.
        # Success! He is redirected to a welcome page.
