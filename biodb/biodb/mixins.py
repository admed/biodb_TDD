from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from biodb import settings
from projects.models import Project


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class LoginPermissionRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            for permission in self.permissions_required:
                if not request.user.has_perm("projects." + permission, permission_obj):
                    _permission = permission.replace('_', ' ')
                    return HttpResponseForbidden(
                        f"<h1>User doesn't have permission: {_permission}</h1>")
            return super().dispatch(request, *args, **kwargs)
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def get_permission_object(self):
        """methtod returning permission object for guardian.

        project_name is required in kwargs else method is returning 404.
        """
        if self.kwargs and 'project_name' in self.kwargs:
            project = get_object_or_404(
                Project, name=self.kwargs['project_name'])
            return project
        return Http404
