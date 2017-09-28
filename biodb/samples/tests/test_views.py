from django.contrib.auth.models import User
from django.test import Client
from io import BytesIO
from openpyxl import load_workbook
from projects.models import Project
from robjects.models import Robject
from samples.models import Sample
from unit_tests.base import FunctionalTest
from samples.views import SampleListView
from guardian.shortcuts import assign_perm

class SampleListViewTest(FunctionalTest):
    def test_anonymous_user_gets_samples_page(self):
        Project.objects.create(name="PROJECT_1")
        response = self.client.get("/projects/PROJECT_1/samples/")
        # redirections to biodb main page
        # it is redirected when using login_required decorator
        # when using LoginRequiredMixin there will be 403
        self.assertEqual(response.status_code, 302)
        # assert that client is still in login page
        self.assertIn('/accounts/login/?next=', response.url)

    def test_render_template_on_get(self):
        user, proj = self.default_set_up_for_robjects_page()
        assign_perm("projects.can_visit_project", user, proj)
        samp = Sample(code='1a2b3c')
        response = self.client.get(f"/projects/{proj.name}/samples/")
        self.assertTemplateUsed(response, "samples/samples_list.html")

    def test_view_get_list_of_samples_and_pass_it_to_context(self):
        user, proj = self.default_set_up_for_robjects_page()
        assign_perm("projects.can_visit_project", user, proj)

        robj = Robject.objects.create(name='robject', project=proj)

        samp1 = Sample.objects.create(code='1a1a', robject=robj)
        samp2 = Sample.objects.create(code='2a2a', robject=robj)
        samp3 = Sample.objects.create(code='3a3a', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/samples/")

        self.assertIn(samp1, response.context["sample_list"])
        self.assertIn(samp2, response.context["sample_list"])
        self.assertIn(samp3, response.context["sample_list"])

    def test_function_used(self):
        user, proj = self.default_set_up_for_robjects_page()
        assign_perm("projects.can_visit_project", user, proj)

        robj = Robject.objects.create(name='robject', project=proj)

        samp1 = Sample.objects.create(code='1a1a', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/samples/")

        self.assertEqual(response.resolver_match.func.__name__,
                         SampleListView.as_view().__name__)

    def test_context_data(self):
        user, proj = self.default_set_up_for_robjects_page()
        assign_perm("projects.can_visit_project", user, proj)

        robj = Robject.objects.create(name='robject', project=proj)

        samp1 = Sample.objects.create(code='1a1a', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/samples/")
        self.assertEqual(proj, response.context['project'])

class SampleDetailViewTest(FunctionalTest):
    def test_anonymous_user_is_redirected_to_login_page(self):
        proj = Project.objects.create(name='Project_1')
        robj = Robject.objects.create(name='Robject', project=proj)
        samp = Sample.objects.create(code='code', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/samples/{samp.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/projects/{proj.name}/samples/{samp.id}/')
