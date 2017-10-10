from django.test import tag
from functional_tests.base import FunctionalTest


@tag('slow')
class RobjectHistoryTestCase(FunctionalTest):
    def get_robject_history_url(self, proj, robj):
        """Method returning History url of robject"""
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/{robj.pk}/history/")

    def test_annonymous_user_visit_history_page(self):
        pass

    def test_user_visit_history_for_created_robject(self):
        # login a user and create a project
        user, proj = self.project_set_up_using_default_data(
            permission_visit=True)
        # create an robject
        robject = Robject.objects.create(name='robject_1', project=proj)
        # User visits history page of the robject
        self.get_robject_history_url(proj, robject)
        pass
