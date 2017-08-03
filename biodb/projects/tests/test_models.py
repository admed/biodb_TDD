from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import models
from django.test import TestCase
from projects.models import Project


class ProjectModelTestCase(TestCase):

    def test_fields_classes(self):
        name_field = Project._meta.get_field("name")
        self.assertIsInstance(name_field, models.CharField)

    def test_proper_name_validation(self):
        proj = Project.objects.create(name="Top Secret")
        msg = "Name must be composed from letters, numbers or underscores."
        with self.assertRaises(ValidationError) as ex:
            proj.full_clean()
        self.assertIn("name", ex.exception.message_dict)
        self.assertIn(msg, ex.exception.message_dict["name"])

    def test_get_absolute_url(self):
        proj = Project.objects.create(name="top_secret")
        self.assertEqual(proj.get_absolute_url(),
                         "/projects/top_secret/robjects/")

    def test_project_name_uniqueness(self):
        Project.objects.create(name="PROJECT_1")
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="PROJECT_1")
