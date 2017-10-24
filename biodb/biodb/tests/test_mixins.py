from django.test import TestCase, RequestFactory
from biodb.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied

# ZASTANOWIĆ SIĘ CZY NIE ZREZYGNOWAĆ Z TEGO ZBIORU TESTÓW.
# TESTY TU ZAWARTE TESTUJĄ IMPLEMENTACJĘ A NIE DZIAŁANIE, WIĘC SĄ ŹLE
# ZAPROJEKTOWANE


# class LoginRequiredMixinTests(TestCase):
#     def test_if_user_is_not_authenticated_method_redirects_to_login_page(self):
#         request = RequestFactory().get("/projects/")
#         request.user = AnonymousUser()
#         with self.assertRaises(PermissionDenied):
#             LoginRequiredMixin().dispatch(request)
#
#     def test_if_user_is_authenticated_metod_calls_super_dispatch(self):
#         user = User.objects.create_user(
#             username="USERNAME", password="PASSWORD")
#         request = RequestFactory().get("/projects/")
#         request.user = user
#
#         class Parent(object):
#             def dispatch(self, request):
#                 return "parent dispatch called"
#
#         class TestClass(LoginRequiredMixin, Parent):
#             pass
#
#         # TestClass dispatch first called, then LoginRequiredMixin's and finally
#         # Parent's
#         result = TestClass().dispatch(request)
#         self.assertEqual(result, "parent dispatch called")
