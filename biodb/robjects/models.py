from django.db import models
from projects.models import Project, Tag
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from projects.models import RelatedModelsCustomManager
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

    def __str__(self):
        return "Robject " + str(self.id)

    @staticmethod
    def get_fields(instance, fields=[]):
        """
        Return dictionary with object fields: {field.verbose_name: field class, ...}
        Attrs:
        """
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

    class Meta:
        unique_together = ("name", "project")

class Name(models.Model):
    name = models.CharField(max_length=100, unique=True)
    objects = RelatedModelsCustomManager()

    def __str__(self):
        return self.name
