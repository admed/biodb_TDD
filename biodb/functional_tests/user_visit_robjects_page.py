from functional_tests.base import FunctionalTest
from projects.models import Project
class UserVisitRobjectsPage(FunctionalTest):
    def test_annonymous_user_visit_robjects_page(self):
        # To visit any robjects page, project object needed.
        Project.objects.create(name="PROJECT_1")
        # Anonymous user goes to robjects page. He sees permission denied
        # message
        self.browser.get(self.live_server_url +
                         "/projects/PROJECT_1/robjects/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(body.text, "403 Forbidden")

    def test_logged_user_visit_robjects_page(self):
        pass
