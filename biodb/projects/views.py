from django.shortcuts import render
from django.views.generic.list import ListView
from projects.models import Project
from django.core.exceptions import PermissionDenied
from biodb.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from projects.models import Tag
from django.shortcuts import redirect
from biodb import settings
from django.core.urlresolvers import reverse
# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


class TagsListView(ListView):
    model = Tag
    template_name = 'projects/tags_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project",
                                     permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project

    def get_queryset(self):
        """
        Overwrite orginal qs and add filtering by project_name
        """
        # original queryset
        qs = super().get_queryset()

        # return filtered qs by project
        return qs.filter(project__name=self.kwargs['project_name'])

    def get_context_data(self, **kwargs):
        context = super(TagsListView, self).get_context_data(**kwargs)
        project = self.kwargs['project_name']
        context['project_name'] = project
        return context


class TagCreateView(CreateView):
    model = Tag
    template_name = 'projects/tag_create.html'
    fields = ['name']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project",
                                     permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project

    def get_context_data(self, **kwargs):
        context = super(TagCreateView, self).get_context_data(**kwargs)
        project = self.kwargs['project_name']
        context['project_name'] = project
        return context

    def form_valid(self, form):
        project_name = self.kwargs['project_name']
        try:
            project = Project.objects.get(name=project_name)
            form.instance.project = project
        except Project.DoesNotExist:
            print('Bla bla')
            raise Http404
        return super(TagCreateView, self).form_valid(form)


class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name']
    pk_url_kwarg = 'tag_id'
    template_name = "projects/tag_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project",
                                     permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project


class TagDeleteView(DeleteView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    template_name = 'projects/tag_delete.html'

    def get_success_url(self):
        return reverse("projects:tag_list", kwargs={"project_name": self.kwargs['project_name']})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            if request.user.has_perm("projects.can_visit_project",
                                     permission_obj):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        project = Project.objects.get(name=self.kwargs['project_name'])
        return project
