from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.http import HttpResponseForbidden


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied


class LoginPermissionRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            permission_obj = self.get_permission_object()
            for permission in self.permissions_required:
                if not request.user.has_perm("projects." + permission, permission_obj):
                    return HttpResponseForbidden(
                        f"<h1>User doesn't have permission: {permission.replace('_', ' ')}</h1>")
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
