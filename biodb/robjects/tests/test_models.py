from django.test import TestCase
from robjects.models import Robject
from django.contrib.auth.models import User
from projects.models import Project
from django.db import models
from robjects.models import Name, Tag


class RobjectModelTestCase(TestCase):
    def test_fields_classes(self):
        project_field = Robject._meta.get_field("project")
        self.assertIsInstance(project_field, models.ForeignKey)

        author_field = Robject._meta.get_field("author")
        self.assertIsInstance(author_field, models.ForeignKey)

        name_field = Robject._meta.get_field("name")
        self.assertIsInstance(name_field, models.CharField)

        create_by_field = Robject._meta.get_field("create_by")
        self.assertIsInstance(create_by_field, models.ForeignKey)

        create_date_field = Robject._meta.get_field("create_date")
        self.assertIsInstance(create_date_field, models.DateTimeField)

        modify_by_field = Robject._meta.get_field("modify_by")
        self.assertIsInstance(modify_by_field, models.ForeignKey)

    def test_str_method(self):
        robj = Robject(id=101)
        self.assertEqual(robj.__str__(), "Robject 101")

    def test_not_string_based_fields_may_be_null(self):
        author_field = Robject._meta.get_field("author")
        project_field = Robject._meta.get_field("project")
        create_by_field = Robject._meta.get_field("create_by")
        create_date_field = Robject._meta.get_field("create_date")
        modify_by_field = Robject._meta.get_field("modify_by")
        self.assertTrue(author_field.null)
        self.assertTrue(project_field.null)
        self.assertTrue(create_by_field.null)
        self.assertTrue(create_date_field.null)
        self.assertTrue(modify_by_field.null)

    def test_related_models_in_foreign_keys(self):
        author_field = Robject._meta.get_field("author")
        project_field = Robject._meta.get_field("project")
        create_by_field = Robject._meta.get_field("create_by")
        modify_by_field = Robject._meta.get_field("modify_by")

        self.assertEqual(author_field.related_model, User)
        self.assertEqual(project_field.related_model, Project)
        self.assertEqual(create_by_field.related_model, User)
        self.assertEqual(modify_by_field.related_model, User)

    def test_related_name_attr_in_create_by_field(self):
        self.assertEqual(
            Robject._meta.get_field("create_by").related_query_name(),
            "robjects_created_by_user")

    def test_Robject_has_tags_field(self):
        try:
            Robject._meta.get_field("tags")
        except models.FieldDoesNotExist:
            self.fail("Robject doesn't have 'tags' field.")

    def test_Robject_has_names_field(self):
        try:
            Robject._meta.get_field("names")
        except models.FieldDoesNotExist:
            self.fail("Robject doesn't have 'names' field.")

    def test_project_field_is_not_blank(self):
        field = Robject._meta.get_field("project")
        self.assertTrue(field.blank)

    def test_create_by_field_is_not_blank(self):
        field = Robject._meta.get_field("create_by")
        self.assertTrue(field.blank)

    def test_create_date_field_is_not_blank(self):
        field = Robject._meta.get_field("create_date")
        self.assertTrue(field.blank)

    def test_modify_by_field_is_not_blank(self):
        field = Robject._meta.get_field("modify_by")
        self.assertTrue(field.blank)

    def test_way_to_get_robjects_related_to_given_tag(self):
        t = Tag.objects.create(name="tag")
        r1 = Robject.objects.create(name="robj_1")
        r1.tags.add(t)
        r2 = Robject.objects.create(name="robj_2")
        r2.tags.add(t)
        robjects = t.robjects.all()
        self.assertEqual(list(robjects), [r1, r2])


class NameModelTestCase(TestCase):
    def test_Name_has_name_field(self):
        try:
            Name._meta.get_field("name")
        except models.FieldDoesNotExist:
            self.fail("Name doesn't have 'name' field.")

    def test_name_field_is_char_field(self):
        self.assertIsInstance(Name._meta.get_field("name"), models.CharField)

    def test_str_method(self):
        n = Name.objects.create(name="hello")
        self.assertEqual(n.__str__(), "hello")


class TagModelTestCase(TestCase):
    def test_Tag_has_name_field(self):
        try:
            Tag._meta.get_field("name")
        except models.FieldDoesNotExist:
            self.fail("Tag doesn't have 'name' field.")

    def test_tag_field_is_char_field(self):
        self.assertIsInstance(Tag._meta.get_field("name"), models.CharField)

    def test_str_method(self):
        t = Tag.objects.create(name="bye")
        self.assertEqual(t.__str__(), "bye")
