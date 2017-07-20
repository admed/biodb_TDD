from functional_tests.base import FunctionalTest
class UserComeToBiodb(FunctionalTest):
    def test_anonymous_user_come_to_biodb(self):
        # Annonymous user come to biodb. He is redirected to login page.
        self.browser.get(self.live_server_url)
        expected_current_url = self.live_server_url + "/accounts/login/"
        self.assertEqual(expected_current_url, self.browser.current_url)

    def test_logged_user_come_to_biodb(self):
        # Logged user come to biodb. He is redirected to projects page.
        self.browser.get(self.live_server_url)
        expected_current_url = self.live_server_url + "/projects/"
        self.assertEqual(expected_current_url, self.browser.current_url)
