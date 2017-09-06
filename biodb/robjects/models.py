from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Robject(models.Model):
    project = models.ForeignKey(to=Project, null=True, blank=True)
    author = models.ForeignKey(
        to=User, null=True, related_name="robjects_in_which_user_is_author")
    name = models.CharField(max_length=100)
    create_by = models.ForeignKey(
        to=User, related_name="robjects_created_by_user", null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    modify_by = models.ForeignKey(to=User, null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="robjects")
    names = models.ManyToManyField("Name", related_name="robjects")
    notes = '<p>These are notes.</p>'
    ref_seq = RichTextField()
    mod_seq = RichTextField()
    description = "<p>This is description.</p>"
    bibliography = '<p>This is bibliography.</p>'
    ref_commercial = RichTextField()
    ref_clinical = RichTextField()
    ligand = models.CharField(max_length=100)
    receptor = models.CharField(max_length=100)

    def __str__(self):
        return "Robject " + str(self.id)


class Name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
