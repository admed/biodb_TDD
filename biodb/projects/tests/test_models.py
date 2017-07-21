from django.core.exceptions import ValidationError
from django.test import TestCase
from projects.models import Project
from django.db import models
from django.db import IntegrityError
from projects.models import Robject


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
        self.assertEqual(p.get_absolute_url(),
                         "/projects/top_secret/robjects/")

    def test_project_name_uniqueness(self):
        Project.objects.create(name="PROJECT_1")
        with self.assertRaises(IntegrityError):
            Project.objects.create(name="PROJECT_1")


class RobjectModelTestCase(TestCase):
    def test_fields_classes(self):
        project_field = Robject._meta.get_field("project")
        self.assertIsInstance(project_field, models.ForeignKey)
        author_field = Robject._meta.get_field("author")
        self.assertIsInstance(author_field, models.ForeignKey)

    def test_str_method(self):
        r = Robject(id=101)
        self.assertEqual(r.__str__(), "Robject 101")
