from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(object):
    def dispatch(self, request):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request)
        raise PermissionDenied
