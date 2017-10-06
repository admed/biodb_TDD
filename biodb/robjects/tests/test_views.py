from unit_tests.base import FunctionalTest
from robjects.models import Robject, Name, Tag
from projects.models import Project
from samples.models import Sample
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_addanother.widgets import AddAnotherWidgetWrapper
from django import forms
from django_addanother.views import CreatePopupMixin
from django.views import generic
from io import BytesIO
from openpyxl import load_workbook
from robjects.views import NameCreateView, TagCreateView
from biodb import settings
from guardian.shortcuts import assign_perm


<<<<<<< Updated upstream
class Robjects_export_to_excel_view_test(FunctionalTest):
    def test_export_to_excel(self):
        # CREATE SAMPLE USER AND PROJECT
        user, proj = self.default_set_up_for_robjects_pages()
        robj = Robject.objects.create(
            author=user, project=proj, name="robject_1")
        # He enters robject raport excel page.
        response = self.client.get(f"/projects/{proj.name}/robjects/excel-raport/")
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical', 'names', 'tags']

        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        self.assertCountEqual(first_row_cells, table_heder_list)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)

    def test_robjects_export_selected_to_excel_view(self):
        # logged user goes to biodb to export a excel file
        user, proj = self.default_set_up_for_robjects_pages()
        robj1 = Robject.objects.create(
            author=user, project=proj, name="robject_1")
        robj2 = Robject.objects.create(
            author=user, project=proj, name="robject_2")

        response = self.client.post(
            f"/projects/{proj.name}/robjects/excel-raport/", {'checkbox': ['1', '2']})
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical']
        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        # check if heaer are the same as first row
        self.assertListEqual(first_row_cells, table_heder_list)

        # check if every robject in different row
        # add +1 because of headers
        self.assertEqual(ws.max_row, Robject.objects.count() + 1)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)


||||||| merged common ancestors
=======
<<<<<<< Updated upstream
||||||| merged common ancestors
class Robjects_export_to_excel_view_test(FunctionalTest):
    def test_export_to_excel(self):
        # logged user goes to biodb to export a excel file
        user, proj = self.default_set_up_for_robjects_page()
        robj = Robject.objects.create(
            author=user, project=proj, name="robject_1")

        response = self.client.get(f"/projects/{proj.name}/robjects/{robj.id}/excel-raport/")
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical', 'files']
        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        self.assertSequenceEqual(first_row_cells, table_heder_list)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)

    def test_robjects_export_selected_to_excel_view(self):
        # logged user goes to biodb to export a excel file
        user, proj = self.default_set_up_for_robjects_page()
        robj1 = Robject.objects.create(
            author=user, project=proj, name="robject_1")
        robj2 = Robject.objects.create(
            author=user, project=proj, name="robject_2")

        response = self.client.post(
            f"/projects/{proj.name}/robjects/excel-raport/", {'checkbox': ['1', '2']})
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical']
        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        # check if heaer are the same as first row
        self.assertListEqual(first_row_cells, table_heder_list)

        # check if every robject in different row
        # add +1 because of headers
        self.assertEqual(ws.max_row, Robject.objects.count() + 1)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)


=======
class Robjects_export_to_excel_view_test(FunctionalTest):
    def test_export_to_excel(self):
        # CREATE SAMPLE USER AND PROJECT
        user, proj = self.default_set_up_for_robjects_page()
        robj = Robject.objects.create(
            author=user, project=proj, name="robject_1")
        # He enters robject raport excel page.
        response = self.client.get(f"/projects/{proj.name}/robjects/{robj.id}/excel-raport/")
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical', 'files']
        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        self.assertSequenceEqual(first_row_cells, table_heder_list)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)

    def test_robjects_export_selected_to_excel_view(self):
        # logged user goes to biodb to export a excel file
        user, proj = self.default_set_up_for_robjects_page()
        robj1 = Robject.objects.create(
            author=user, project=proj, name="robject_1")
        robj2 = Robject.objects.create(
            author=user, project=proj, name="robject_2")

        response = self.client.post(
            f"/projects/{proj.name}/robjects/excel-raport/", {'checkbox': ['1', '2']})
        # assert attachment name as report.xlsx
        self.assertEqual(response.get('Content-Disposition'),
                         "attachment; filename=report.xlsx")

        table_heder_list = ['id', 'project', 'author', 'name', 'create_by',
                            'create_date', 'modify_date', 'modify_by', 'notes',
                            'ligand', 'receptor', 'ref_seq', 'mod_seq',
                            'description', 'bibliography', 'ref_commercial',
                            'ref_clinical']
        # assert headers are the same as robject atrinutes names
        with BytesIO(response.content) as f:
            self.assertIsNotNone(f)
            wb = load_workbook(f)
            ws = wb.active
            first_row_cells = []
            for row in ws.rows:
                for cell in row:
                    first_row_cells.append(cell.value)
                break
        # check if heaer are the same as first row
        self.assertListEqual(first_row_cells, table_heder_list)

        # check if every robject in different row
        # add +1 because of headers
        self.assertEqual(ws.max_row, Robject.objects.count() + 1)

        # if status code of requeszt is 200 -
        # The request was successfully received,
        # understood, and accepted
        self.assertEqual(response.status_code, 200)


>>>>>>> Stashed changes
>>>>>>> Stashed changes
class RobjectSamplesListTest(FunctionalTest):
    def test_anonymous_user_gets_samples_page(self):
        proj = Project.objects.create(name="PROJECT_1")
        Robject.objects.create(name="Robject_1", project=proj)
        response = self.client.get("/projects/PROJECT_1/robjects/1/samples/")
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/?next=', response.url)

    def test_render_template_on_get(self):
        user, proj = self.default_set_up_for_robjects_pages()
        robj = Robject.objects.create(name="rob")
        assign_perm("projects.can_visit_project", user, proj)
        samp = Sample(code='1a2b3c')
        response = self.client.get(f"/projects/{proj.name}/robjects/{robj.id}/samples/")
        self.assertTemplateUsed(response, "samples/samples_list.html")

    def test_view_get_list_of_samples_and_pass_it_to_context(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_visit_project", user, proj)

        robj = Robject.objects.create(name='robject', project=proj)

        samp1 = Sample.objects.create(code='1a1a', robject=robj)
        samp2 = Sample.objects.create(code='2a2a', robject=robj)
        samp3 = Sample.objects.create(code='3a3a', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/robjects/{robj.id}/samples/")

        self.assertIn(samp1, response.context["sample_list"])
        self.assertIn(samp2, response.context["sample_list"])
        self.assertIn(samp3, response.context["sample_list"])

    def test_context_data(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_visit_project", user, proj)

        robj = Robject.objects.create(name='robject', project=proj)

        samp1 = Sample.objects.create(code='1a1a', robject=robj)
        response = self.client.get(f"/projects/{proj.name}/robjects/{robj.id}/samples/")
        self.assertEqual(proj, response.context['project'])


class RObjectsListViewTests(FunctionalTest):
    def test_anonymous_user_gets_robjects_page(self):
        Project.objects.create(name="PROJECT_1")
        response = self.client.get("/projects/PROJECT_1/robjects/")
        self.assertEqual(response.status_code, 403)

    def test_render_template_on_get(self):
        user, proj = self.default_set_up_for_robjects_pages()
        response = self.client.get(f"/projects/{proj.name}/robjects/")

        self.assertTemplateUsed(response, "projects/robjects_list.html")

    def test_view_create_list_of_robjects_and_pass_it_to_context(self):
        user, proj = self.default_set_up_for_robjects_pages()

        robj1 = Robject.objects.create(author=user, project=proj)
        robj2 = Robject.objects.create(author=user, project=proj)
        robj3 = Robject.objects.create(author=user, project=proj)
        response = self.client.get(f"/projects/{proj.name}/robjects/")

        self.assertIn(robj1, response.context["robject_list"])
        self.assertIn(robj2, response.context["robject_list"])


class SearchRobjectsViewTests(FunctionalTest):
    def test_view_renders_robjects_page_template(self):
        user, proj = self.default_set_up_for_robjects_pages()

        response = self.client.get(f"/projects/{proj.name}/robjects/search/",
                                   {"query": ""})
        self.assertTemplateUsed(response, "projects/robjects_list.html")

    def test_view_gets_valid_query_on_get__view_pass_qs_to_template(self):
        user, proj = self.default_set_up_for_robjects_pages()

        robject_1 = Robject.objects.create(name="robject_1", project=proj)
        robject_2 = Robject.objects.create(name="robject_2", project=proj)

        response = self.client.get(
            f"/projects/{proj.name}/robjects/search/", {"query": "robject_1"})
        queryset = Robject.objects.filter(name="robject_1")
        # comparison of two querysets
        self.assertQuerysetEqual(
            response.context["robject_list"], map(repr, queryset))

    def test_annonymous_user_has_no_access_to_search_view(self):
        proj = Project.objects.create(name="project_1")

        resp = self.client.get(f"/projects/{proj.name}/robjects/search/")
        self.assertEqual(resp.status_code, 403)

    def test_view_can_perform_search_basing_on_part_of_robject_name(self):
        user, proj = self.default_set_up_for_robjects_pages()

        robject_1 = Robject.objects.create(name="robject_1", project=proj)
        robject_2 = Robject.objects.create(name="robject_2", project=proj)

        response = self.client.get(
            f"/projects/{proj.name}/robjects/search/", {"query": "object_1"})  # part!

        queryset = Robject.objects.filter(name="robject_1")

        # comparison of two querysets
        self.assertQuerysetEqual(
            response.context["robject_list"], map(repr, queryset))

    def test_search_is_case_insensitive(self):
        user, proj = self.default_set_up_for_robjects_pages()

        robj = Robject.objects.create(name="RoBjEcT_1", project=proj)

        # lower case query
        resp = self.client.get(
            f"/projects/{proj.name}/robjects/search/", {"query": "robject_1"})

        self.assertEqual(list(resp.context["robject_list"]),
                         [robj])

        # upper case query
        resp = self.client.get(
            f"/projects/{proj.name}/robjects/search/", {"query": "ROBJECT_1"})

        self.assertEqual(list(resp.context["robject_list"]),
                         [robj])

    def test_view_pass_project_name_to_context(self):
        user, proj = self.default_set_up_for_robjects_pages()

        resp = self.client.get(f"/projects/{proj.name}/robjects/search/",
                               {"query": "robject_1"})

        self.assertEqual(proj.name, resp.context["project_name"])

    def create_sample_robject_and_send_query_to_search_view(self, project,
                                                            query,
                                                            **robject_kwargs):

        robj = Robject.objects.create(project=project, **robject_kwargs)
        resp = self.client.get(f"/projects/{project.name}/robjects/search/",
                               {"query": query})
        return robj, resp

    def create_sample_robject_search_for_it_and_confirm_results(
            self, query, robject_kwargs):
        user, proj = self.default_set_up_for_robjects_pages()

        robj, resp = self.create_sample_robject_and_send_query_to_search_view(
            project=proj, query=query, **robject_kwargs)

        self.assertIn(robj, resp.context["robject_list"])

    def test_search_include_full_author_username(self):
        robject_kwargs = {
            "author": User.objects.create_user(username="AUTHOR")
        }
        self.create_sample_robject_search_for_it_and_confirm_results(
            query="AUTHOR",
            robject_kwargs=robject_kwargs
        )

    def test_search_include_fragment_author_username(self):
        robject_kwargs = {
            "author": User.objects.create_user(username="AUTHOR")
        }
        self.create_sample_robject_search_for_it_and_confirm_results(
            query="AUTH",
            robject_kwargs=robject_kwargs
        )

    def test_search_include_case_insensitive_full_author_username(self):
        robject_kwargs = {
            "author": User.objects.create_user(username="AUTHOR")
        }
        self.create_sample_robject_search_for_it_and_confirm_results(
            query="aUtHoR",
            robject_kwargs=robject_kwargs
        )

    def test_empty_query_will_display_all_robjects(self):
        user, proj = self.default_set_up_for_robjects_pages()

        robj_1 = Robject.objects.create(project=proj)
        robj_2 = Robject.objects.create(project=proj)

        resp = self.client.get(
            f"/projects/{proj.name}/robjects/search/", {"query": ""})

        all_robjects = Robject.objects.filter(project=proj)

        self.assertEqual(
            list(resp.context["robject_list"]),
            list(all_robjects)
        )

    def test_search_include_robjects_from_given_project(self):
        user, proj = self.default_set_up_for_robjects_pages()

        other_proj = Project.objects.create(name="other_proj")
        robj = Robject.objects.create(project=other_proj, name="robj")

        resp = self.client.get(
            f"/projects/{proj.name}/robjects/search/",
            {"query": f"{robj.name}"})

        self.assertNotIn(
            robj,
            list(resp.context["robject_list"])
        )


class RobjectCreateViewTestCase(FunctionalTest):
    def get_robject_create_url(self, proj):
        return reverse("projects:robjects:robject_create", kwargs={"project_name": proj.name})

    def get_form_from_context(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.get(
            reverse("projects:robjects:robject_create", kwargs={"project_name": proj.name}))
        form = response.context["form"]

        return form

    def test_renders_template(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.get(
            reverse("projects:robjects:robject_create", args=(proj.name,)))
        self.assertTemplateUsed(
            response, template_name="robjects/robject_create.html")

    def test_renders_form_in_context(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.get(
            reverse("projects:robjects:robject_create", args=(proj.name,)))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_model_class_is_Robject_in_form(self):
        form = self.get_form_from_context()
        self.assertEqual(form._meta.model, Robject)

    def test_widget_instance_of_names_field_in_form(self):
        form = self.get_form_from_context()
        self.assertIsInstance(
            form.base_fields["names"].widget, AddAnotherWidgetWrapper)

    def test_names_widget_arguments_in_form(self):
        form = self.get_form_from_context()
        widget = form.base_fields["names"].widget.widget
        add_related_url = form.base_fields["names"].widget.add_related_url
        self.assertIsInstance(widget, forms.SelectMultiple)
        self.assertEqual(add_related_url, reverse(
            "projects:robjects:names_create", args=(Project.objects.last().name,)))

    def test_widget_instance_of_tags_field_in_form(self):
        form = self.get_form_from_context()
        self.assertIsInstance(
            form.base_fields["tags"].widget, AddAnotherWidgetWrapper)

    def test_tags_widget_arguments_in_form(self):
        form = self.get_form_from_context()
        widget = form.base_fields["tags"].widget.widget
        add_related_url = form.base_fields["tags"].widget.add_related_url
        self.assertIsInstance(widget, forms.SelectMultiple)
        self.assertEqual(add_related_url, reverse(
            "projects:robjects:tags_create", args=(Project.objects.last().name,)))

    def test_view_redirects_to_robject_list_page_on_post(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.post(
            self.get_robject_create_url(proj),
            data={"name": "whatever"}
        )
        self.assertRedirects(response, reverse(
            "projects:robjects:robjects_list", args=(proj.name,)))

    def test_name_field_is_required(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.post(
            self.get_robject_create_url(proj),
            data={"hello": "world"}  # request.POST pass, form.is_valid() fails
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.get_robject_create_url(proj),
            data={"name": "whatever"}
        )

        self.assertEqual(response.status_code, 302)

    def test_annonymous_user_is_redirect_to_login_page_on_get(self):
        proj = Project.objects.create(name="proj")
        response = self.client.get(self.get_robject_create_url(proj))

        self.assertRedirects(
            response,
            settings.LOGIN_URL + "?next=" + self.get_robject_create_url(proj)
        )

    def test_annonymous_user_is_redirect_to_login_page_on_post(self):
        proj = Project.objects.create(name="proj")
        response = self.client.post(self.get_robject_create_url(proj), data={})

        self.assertRedirects(
            response,
            settings.LOGIN_URL + "?next=" + self.get_robject_create_url(proj)
        )

    def test_user_without_project_mod_permission_gets_403_on_get(self):
        user, proj = self.default_set_up_for_robjects_pages()
        response = self.client.get(self.get_robject_create_url(proj))

        self.assertEqual(response.status_code, 403)

    def test_view_removes_all_robject_less_names_on_get(self):
        Name.objects.create(name="name_1")
        Name.objects.create(name="name_2")
        self.assertEqual(Name.objects.filter(robjects=None).count(), 2)
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        self.client.get(self.get_robject_create_url(proj))
        self.assertEqual(Name.objects.filter(robjects=None).count(), 0)

    def test_rendered_form_has_no_create_by_field(self):
        form = self.get_form_from_context()
        self.assertNotIn("create_by", form.fields)

    def test_rendered_form_has_no_modify_by_field(self):
        form = self.get_form_from_context()
        self.assertNotIn("modify_by", form.fields)

    def test_rendered_form_has_no_create_date_field(self):
        form = self.get_form_from_context()
        self.assertNotIn("create_date", form.fields)

    def test_rendered_form_has_no_modify_date_field(self):
        form = self.get_form_from_context()
        self.assertNotIn("modify_date", form.fields)

    def test_view_assign_create_by_to_new_robject(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.post(
            self.get_robject_create_url(proj), {"name": "test"})
        r = Robject.objects.last()
        self.assertEqual(r.create_by, user)

    def test_view_assign_modify_by_to_new_robject(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("projects.can_modify_project", user, proj)
        response = self.client.post(
            self.get_robject_create_url(proj), {"name": "test"})
        r = Robject.objects.last()
        self.assertEqual(r.modify_by, user)

    def test_project_field_from_context_form_is_hidden(self):
        form = self.get_form_from_context()
        self.assertTrue(form.fields["project"].widget.is_hidden)

    def test_project_field_from_context_form_initial(self):
        form = self.get_form_from_context()
        self.assertEqual(form.initial, {"project": Project.objects.first()})


class NameCreateViewTestCase(FunctionalTest):
    def get_names_create_url(self, proj):
        url = reverse("projects:robjects:names_create",
                      kwargs={"project_name": proj.name})
        return url

    def get_robject_create_url(self, proj):
        return reverse("projects:robjects:robject_create", args=(proj.name,))

    def test_view_parents(self):
        self.assertEqual(NameCreateView.__bases__,
                         (CreatePopupMixin, generic.CreateView))

    def test_view_model_attr(self):
        self.assertEqual(NameCreateView.model, Name)

    def test_view_fields_attr(self):
        self.assertEqual(NameCreateView.fields, "__all__")

    def test_render_template(self):
        proj = Project.objects.create(name="proj_1")
        response = self.client.get(
            self.get_names_create_url(proj),
            HTTP_REFERER=self.get_robject_create_url(proj))
        self.assertTemplateUsed(response, "robjects/names_create.html")

    def test_view_return_400_when_requested_using_url(self):
        proj = Project.objects.create(name="proj_1")

        # Note: when form is open in popup window, request contains HTTP_REFERER
        # key in request.META dictionary. Otherwise, key doesn't exists.
        # HTTP_REFERER holds url to page from popup is open.

        # Test view gets request object without "HTTP_REFERER" key.
        response = self.client.get(self.get_names_create_url(proj))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "<h1>Error 400</h1><p>Form available from robject form only</p>",
            response.content.decode())

        # Test view gets request with META["HTTP_REFERER"].
        response = self.client.get(
            self.get_names_create_url(proj),
            HTTP_REFERER=self.get_robject_create_url(proj))
        self.assertEqual(response.status_code, 200)


class TagCreateViewTestCase(FunctionalTest):
    def get_tags_create_url(self, proj):
        url = reverse("projects:robjects:tags_create",
                      kwargs={"project_name": proj.name})
        return url

    def get_robject_create_url(self, proj):
        return reverse("projects:robjects:robject_create", args=(proj.name,))

    def test_view_parents(self):
        self.assertEqual(TagCreateView.__bases__,
                         (CreatePopupMixin, generic.CreateView))

    def test_view_model_attr(self):
        self.assertEqual(TagCreateView.model, Tag)

    def test_render_template(self):
        proj = Project.objects.create(name="proj_1")
        response = self.client.get(reverse("projects:robjects:tags_create", kwargs={
                                   "project_name": proj.name}), HTTP_REFERER=self.get_robject_create_url(proj))
        self.assertTemplateUsed(response, "robjects/tags_create.html")

    def test_view_renders_form_without_project_field(self):
        proj = Project.objects.create(name="proj_1")
        response = self.client.get(reverse("projects:robjects:tags_create", kwargs={
                                   "project_name": proj.name}), HTTP_REFERER=self.get_robject_create_url(proj))
        self.assertNotIn("project", response.context["form"].fields)

    def test_project_is_assigned_automatically_in_view(self):
        proj = Project.objects.create(name="proj_1")
        self.client.post(
            reverse("projects:robjects:tags_create", kwargs={"project_name": proj.name}), data={"name": "tag_name"},
            HTTP_REFERER=self.get_robject_create_url(proj))
        t = Tag.objects.last()
        self.assertEqual(t.name, "tag_name")
        self.assertEqual(t.project, proj)

    def test_view_return_400_when_requested_using_url(self):
        proj = Project.objects.create(name="proj_1")

        # Note: when form is open in popup window, request contains HTTP_REFERER
        # key in request.META dictionary. Otherwise, key doesn't exists.
        # HTTP_REFERER holds url to page from popup is open.

        # Test view gets request object without "HTTP_REFERER" key.
        response = self.client.get(self.get_tags_create_url(proj))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "<h1>Error 400</h1><p>Form available from robject form only</p>",
            response.content.decode())

        # Test view gets request with META["HTTP_REFERER"].
        response = self.client.get(
            self.get_tags_create_url(proj),
            HTTP_REFERER=self.get_robject_create_url(proj))
        self.assertEqual(response.status_code, 200)


class RobjectDeleteTestCase(FunctionalTest):
    def default_set_up_for_robject_delete(self):
        user, proj = self.default_set_up_for_robjects_pages()
        assign_perm("can_delete_robjects", user, proj)
        return proj

    def test_annonymous_user_is_redirect_to_login_page(self):
        self.annonymous_testing_helper(
            self.ROBJECT_DELETE_URL, self.ROBJECT_LIST_URL)

    def test_view_refuse_access_to_users_without_both_permissions(self):
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        response = self.client.get(self.ROBJECT_DELETE_URL)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>User doesn't have permission to access this page.</h1>",
                         response.content.decode("utf-8"))

    def test_view_refuse_access_to_users_without_robject_delete_permission(self):
        self.other_permission_testing_helper(
            self.ROBJECT_DELETE_URL,
            "User doesn't have permission to access this page.")

    def test_view_refuse_access_to_users_without_project_visit_permission(self):
        user = self.default_set_up_for_projects_pages()
        proj = Project.objects.create(name="project_1")
        assign_perm("projects.can_delete_robjects", user, proj)
        response = self.client.get(self.ROBJECT_DELETE_URL)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(f"<h1>User doesn't have permission to access this page.</h1>",
                         response.content.decode("utf-8"))

    def test_view_renders_delete_confirmattion_template(self):
        self.default_set_up_for_robject_delete()
        response = self.client.get(self.ROBJECT_DELETE_URL)
        self.assertTemplateUsed(
            response, "robjects/robject_confirm_delete.html")

    def test_view_redirects_on_post(self):
        self.default_set_up_for_robject_delete()
        response = self.client.post(self.ROBJECT_DELETE_URL)
        self.assertRedirects(response, self.ROBJECT_LIST_URL)

    def test_view_add_delete_robjects_to_context(self):
        proj = self.default_set_up_for_robject_delete()
        robj_1 = Robject.objects.create(name="robject_1", project=proj)
        robj_2 = Robject.objects.create(name="robject_2", project=proj)
        response = self.client.get(self.ROBJECT_DELETE_URL, {
            robj_1.name: robj_1.id,
            robj_2.name: robj_2.id
        })
        robjects_context = response.context["robjects"]
        self.assertEqual(len(robjects_context), 2)
        self.assertIn(robj_1, robjects_context)
        self.assertIn(robj_2, robjects_context)
