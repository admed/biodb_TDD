from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
# Create your models here.


class Robject(models.Model):
    project = models.ForeignKey(to=Project, null=True)
    author = models.ForeignKey(
        to=User, null=True, related_name="robjects_in_which_user_is_author")
    name = models.CharField(max_length=100)
    create_by = models.ForeignKey(
        to=User, related_name="robjects_created_by_user", null=True)
    create_date = models.DateTimeField(null=True)
    modify_by = models.ForeignKey(to=User, null=True)
    tags = models.ManyToManyField("Tag")
    names = models.ManyToManyField("Name")

    def __str__(self):
        return "Robject " + str(self.id)


class Name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    pass
