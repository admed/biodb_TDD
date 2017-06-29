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
        inputs = login_form.find_elements_by_tag_name("input")
        inputs_id = [input_.get_attribute("id") for input_ in inputs]
        for ID in ["login_input", "password_input"]:
            self.assertIn(ID, inputs_id)

        self.fail("Finish test!")

        # Excited user clicks sign up link. He noticed new form with several
        # fields: username, email adress, password and repeat password.

        # Distracted user accidentaly clicks submit button before fill any
        # field. Every field is requried so now he sees error messages bound
        # with any field.

        # Immediately decides to repair his mistake and starts to fill the form
        # with data. But he dont know that user with such username, email and
        # password already exists in database. He quickly learns about it when
        # he clicks submit button. Above every field now appear message with
        # appropriate message: 'user with such <field> already exists'.

        # User fills form with new data and clicks submit button once again.
        # Success! He is redirected to a welcome page.
