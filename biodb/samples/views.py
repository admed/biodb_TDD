"""Views for robject search."""
import re
from biodb.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from biodb.mixins import LoginRequiredMixin
from django_tables2 import RequestConfig
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic.list import ListView
from projects.models import Project
from robjects.models import Robject
from samples.models import Sample
from samples.tables import SampleTable
from django_tables2 import SingleTableView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from biodb import settings
# from samples.forms import RobjectSelectFrom


# @method_decorator(login_required, name='dispatch')
class SampleListView(SingleTableView, ListView):
    model = Sample
    template_name = "samples/samples_list.html"
    table_class = SampleTable

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project", permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project

    def get(self, request, project_name, *args, **kwargs):
        """A base view for displaying a list of objects."""
        try:
            # print(dir(self.request.seesion))
            request.session['_succes_url'] = self.request.build_absolute_uri()
            project = Project.objects.get(name=project_name)
            # add project to view attributes
            self.project = project
        except Robject.DoesNotExist:
            raise Http404
        return super(SampleListView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        """
        Overwrite orginal qs and add filtering by robject
        """
        # original queryset
        qs = super(SampleListView, self).get_queryset()

        qs = qs.filter(robject__project=self.project)
        return qs

    def get_context_data(self):
        context = super(SampleListView, self).get_context_data()
        # print(context)
        context['project'] = self.project
        return context


class SampleDetailView(DetailView):
    model = Sample
    template_name = 'samples/sample_details.html'
    pk_url_kwarg = "sample_id"

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project", permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get(self, request, *args, **kwargs):
        """A base view for displaying a list of objects."""
        # check if project exists
        try:

            sample_id = kwargs['sample_id']
            sample = Sample.objects.get(id=sample_id)
            # add project to view attributes
            self.sample = sample
        except Sample.DoesNotExist:
            raise Http404
        return super(SampleDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sample'] = self.sample
        return context