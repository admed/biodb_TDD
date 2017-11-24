from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from projects.models import RelatedModelsCustomManager
from simple_history.models import HistoricalRecords
from django.core.urlresolvers import reverse
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
    tags = models.ManyToManyField("Tag", related_name="robjects", blank=True)
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

    @staticmethod
    def get_fields(instance, fields=None):
        """
        Return dictionary with object fields: {field.verbose_name: field class}
        Attrs:
        """
        if not fields:
            fields = []
        fields_dict = {field.verbose_name: getattr(
            instance, field.name) for field in instance._meta.get_fields() if field.name in fields}
        return sorted(fields_dict.items())

    def get_general_fields(self):
        '''
            Return fields : id, create_date, create_by, modify_date, modify_by, author
        '''
        fields = ["id", "create_date", "create_by",
                  "modify_date", "modify_by", "author"]
        return self.get_fields(self, fields)

    def get_detail_fields(self):
        '''
            Return fields: ligand, receptor, ref_seq, mod_seq,
            description, bibliography, ref_commercial, ref_clinical, notes
        '''
        fields = ["ligand", "receptor", "ref_seq", "mod_seq", "description",
                  "bibliography", "ref_commercial", "ref_clinical", "notes"]
        return self.get_fields(self, fields)

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

    @property
    def _history_user(self):
        return self.modify_by

    @_history_user.setter
    def _history_user(self, value):
        self.modify_by = value


class Name(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = RelatedModelsCustomManager()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(to=Project, related_name="tags", null=True)
    objects = RelatedModelsCustomManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:tag_list", kwargs={"project_name": self.project.name})
