from django.core.exceptions import ValidationError
from django.test import TestCase
from projects.models import Project
from django.db import models
class ProjectModelTestCase(TestCase):

    def test_fields_classes(self):
        name_field = Project._meta.get_field("name")
        self.assertIsInstance(name_field, models.CharField)

    def test_proper_name_validation(self):
        p = Project.objects.create(name="Top Secret")
        msg = "Name must be composed from letters, numbers or underscores."
        with self.assertRaises(ValidationError) as ex:
            p.full_clean()
        self.assertIn("name", ex.exception.message_dict)
        self.assertIn(msg, ex.exception.message_dict["name"])

    def test_get_absolute_url(self):
        p = Project.objects.create(name="top_secret")
        self.assertEqual(p.get_absolute_url(), "/projects/top_secret/robjects/")
