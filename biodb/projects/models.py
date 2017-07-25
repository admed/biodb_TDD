from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def clean(self):
        allowed_name_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy\
z0123456789_"
        msg = "Name must be composed from letters, numbers or underscores."
        for char in self.name:
            if char not in allowed_name_chars:
                raise ValidationError({"name": msg})

    def get_absolute_url(self):
        return "/projects/%s/robjects/" % self.name


class Robject(models.Model):
    project = models.ForeignKey(to=Project, null=True)
    author = models.ForeignKey(
        to=User, null=True, related_name="robjects_in_which_user_is_author")
    name = models.CharField(max_length=100)
    create_by = models.ForeignKey(
        to=User, related_name="robjects_created_by_user")
    create_date = models.DateTimeField()
    modify_by = models.ForeignKey(to=User)

    def __str__(self):
        return "Robject " + str(self.id)
