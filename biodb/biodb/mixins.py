from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from biodb import settings


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
