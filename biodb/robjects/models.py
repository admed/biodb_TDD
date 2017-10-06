from django.db import models
from projects.models import Project, Tag
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords
# Create your models here.


class Robject(models.Model):
    project = models.ForeignKey(to=Project, null=True, blank=True)
    author = models.ForeignKey(
        to=User, blank=True, null=True, related_name="robjects_in_which_user_is_author")
    name = models.CharField(max_length=100, null=True)
    create_by = models.ForeignKey(
        to=User, related_name="robjects_created_by_user", null=True, blank=True)
    create_date = models.DateTimeField(
        null=True, blank=True, auto_now_add=True)
    modify_by = models.ForeignKey(to=User, null=True, blank=True)
    modify_date = models.DateTimeField(null=True, auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="robjects", blank=True)
    names = models.ManyToManyField("Name", related_name="robjects", blank=True)
    notes = RichTextField(blank=True)
    ref_seq = RichTextField(blank=True)
    mod_seq = RichTextField(blank=True)
    description = RichTextField(blank=True)
    bibliography = RichTextField(blank=True)
    ref_commercial = RichTextField(blank=True)
    ref_clinical = RichTextField(blank=True)
    ligand = models.CharField(max_length=100, blank=True)
    receptor = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return "Robject " + str(self.id)

    class Meta:
        unique_together = ("name", "project")

    @property
    def _history_user(self):
        return self.modify_by

    @_history_user.setter
    def _history_user(self, value):
        self.modify_by = value

    def get_fields(self, exclude=None):
        """This method return list of model fields reduced by exclude list."""
        # create set from input list | remove duplicates the same time
        if not exclude:
            excludes = []
        else:
            excludes = set(exclude)
        # get set from model dict keys
        fields = set(self.__dict__.keys())
        # return difference set
        return fields.difference(excludes)

class Name(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
