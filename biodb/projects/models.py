# from django.contrib.auth.models import User
import string
from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def clean(self):
        """
        Extra cleaning of name chars in Forms.
        Any ValidationError raised by this method will be associated
        with the 'name' field;
        """
        allowed_name_chars = string.ascii_letters + string.digits + '_-'
        msg = "Name must be composed from letters, numbers or underscores."
        for char in self.name:
            if char not in allowed_name_chars:
                raise ValidationError({"name": msg})

    def get_absolute_url(self):
        return "/projects/%s/robjects/" % self.name

    class Meta:
        permissions = (
            ("can_visit_project", "User can see project elements."),
            ("can_modify_project", "User can modify project elements."))


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(to=Project, related_name="tags")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:tag_list", kwargs={"project_name": self.project.name})
