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

    def get_fields_names(self, exclude=None, relation=False):
        """This method return set of model fields.

        All fields are received automatically from model.
        By default relational fields are not included.

        Args:
            exclude (:obj:`list` or `set`): list of names of fields to exclude.
            relation (bool): True include relational fields. Defaults: False.

        Returns:
            :obj:`set`: Set containing model fields names.
        """
        # create set from input list | remove duplicates the same time
        if not exclude:
            excludes = set()
        else:
            excludes = set(exclude)
        # get set from model dict keys
        if relation:
            fields = set(f.name for f in self._meta.get_fields())
        else:
            fields = set(f.name for f in self._meta.get_fields()
                         if not (f.is_relation or f.one_to_one or
                                 (f.many_to_one and f.related_model)))
        # return difference set
        return fields.difference(excludes)


class Name(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
