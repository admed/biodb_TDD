"""Views for robject search."""
import re
from biodb.mixins import LoginRequiredMixin
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import TextField
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import View, CreateView
from projects.models import Project
from robjects.models import Robject, Name, Tag
from django import forms
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django_addanother.views import CreatePopupMixin
from guardian.mixins import LoginRequiredMixin as GuardianLoginRequiredMixin
from guardian.mixins import PermissionRequiredMixin
from biodb import settings
# Create your views here.


def robjects_list_view(request, project_name):
    if not request.user.is_authenticated():
        raise PermissionDenied
    project = Project.objects.get(name=project_name)
    robject_list = Robject.objects.filter(project=project)
    return render(request, "projects/robjects_list.html",
                  {"robject_list": robject_list, "project_name": project_name})


# TODO: Add multipleObjectMixin to inherit by this class??
class SearchRobjectsView(LoginRequiredMixin, View):
    """View to show filtered list of objects."""
    model = Robject

    def get(self, request, project_name):
        query = request.GET.get("query")

        queryset = self.perform_search(query, project_name)

        return render(request, "projects/robjects_list.html",
                      {"robject_list": queryset, "project_name": project_name})

    def normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        """Splits the query string in invidual keywords, getting rid of
           unecessary spaces and grouping quoted words together.

            Args:
                query_string (str): string with query words

            Example:
                >>> normalize_query('some random  words "with   quotes  "
                                    and   spaces  ')
                ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

            Returns:
                the list of words
        """
        terms = [normspace(
            ' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
        return terms

    def perform_search(self, query, project_name):
        """Perform search for robjects using given query.

        Normalize search string and divede them into search terms.
        Create list of search queris for CharField and TextField.

        Args:
            query (str): Search string provieded by user
            project_name (str): name of the project (auto).

        Returns:
            model objects list (list): filtered list of model objects
            model is filtered based on Q objects Complex SQL expression
            in Django (see Django docs) and project_name
        """
        # normalize query string and get the list of words (search terms)
        terms = self.normalize_query(query)
        # get list of text fields
        text_fields = [f for f in self.model._meta.get_fields() if isinstance(
            f, (CharField, TextField))]
        # get the list of foreig fields
        foreign_fields = [
            f for f in self.model._meta.get_fields()
            if isinstance(f, ForeignKey)]
        # get dict with ForeigKey field as key and list of Char/Text fields
        # that are in related model as a argument
        foreign_models_fields = {}
        for foreign_field in foreign_fields:
            fmodel = self.model._meta.get_field(
                '%s' % foreign_field.name).rel.to
            foreign_models_fields[foreign_field] = [
                f for f in fmodel._meta.fields
                if isinstance(f, (CharField, TextField))]

        # define Q() objects to use or on queries
        qs = Q()
        # iterate over all search terms and create the queries
        # for model text fields and foreign text fields
        for term in terms:
            # get queries for Char/Text fields
            queries = [Q(**{'%s__icontains' % f.name: term})
                       for f in text_fields]
            # exted queries by foreign fields
            if foreign_models_fields:
                for foreign_field, model_fields \
                        in foreign_models_fields.items():
                    queries += [Q(**{'%s__%s__icontains' %
                                     (foreign_field.name, f.name): term})
                                for f in model_fields]
            # perform logical OR on queries
            if queries:
                for qs_query in queries:
                    qs = qs | qs_query
        # project required

        return self.model.objects.filter(qs, project__name=project_name)


class RobjectCreateView(CreateView):
    model = Robject
    template_name = "robjects/robject_create.html"
    # raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_modify_project", permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_form_class(self):
        form = forms.modelform_factory(
            model=Robject, fields="__all__",
            exclude=["create_by", "create_date", "modify_by"],
            widgets={
                "names": AddAnotherWidgetWrapper(
                    widget=forms.SelectMultiple,
                    add_related_url=reverse(
                        "names_create", args=(self.args[0],))
                ),
                "tags":  AddAnotherWidgetWrapper(
                    widget=forms.SelectMultiple,
                    add_related_url=reverse(
                        "tags_create", args=(self.args[0],))
                ),
                'project': forms.HiddenInput()
            })
        return form

    def get_success_url(self):
        return reverse("robjects_list", args=(self.args[0],))

    def get_permission_object(self):
        project = Project.objects.get(name=self.args[0])
        return project

    def get(self, request, *args, **kwargs):
        Name.objects.filter(robjects=None).delete()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        robject = form.save()
        robject.create_by = self.request.user
        robject.modify_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {
            "project": Project.objects.get(name=self.args[0])
        }


class NameCreateView(CreatePopupMixin, CreateView):
    model = Name
    fields = "__all__"
    template_name = "robjects/names_create.html"


class TagCreateView(CreatePopupMixin, CreateView):
    model = Tag
    fields = ["name"]
    template_name = "robjects/tags_create.html"
    success_url = "/"  # not required, for test pass purpose only!

    def form_valid(self, form):
        tag = form.save()
        tag.project = Project.objects.get(name=self.args[0])
        return super().form_valid(form)
