from functional_tests.base import FunctionalTest


class StaticFilesTests(FunctionalTest):
    def test_login_page(self):
        # User goes to login page.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # He noticed that login form is nicely centered.
        login_button = self.browser.find_element_by_id("submit_button")
        self.assertAlmostEqual(
            login_button.location["x"] + login_button.size["width"]/2,
            512,
            delta=10
        )
