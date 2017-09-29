# import time
# from datetime import datetime
import time
from datetime import datetime
from django.contrib.auth.models import User
from django.test import tag
from functional_tests.base import FunctionalTest
from projects.models import Project
from projects.models import Tag
from robjects.models import Robject
from selenium.common.exceptions import NoSuchElementException
from guardian.shortcuts import assign_perm

class TagCreateTestCase(FunctionalTest):
    def get_tag_list(self, proj):
        self.browser.get(self.live_server_url +
                         f"/projects/{proj.name}/tags/create/")

    def test_annonymous_user_visits_tags_list(self):
        # CREATE SAMPLE RPOJECT.
        proj = Project.objects.create(name="project_1")
        # Annonymus user can not visit tag create page.
        self.get_tag_list(proj)
        # He can not enter requested url.
        # He is still on home page of biodb.
        current_url = self.browser.current_url
        expected_url = self.live_server_url + f"/accounts/login/?next=/projects/{proj.name}/tags/create/"
        self.assertEqual(current_url, expected_url)
