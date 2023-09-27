from django.db import models
from django.conf import settings


class Project(models.Model):

    class Type(models.TextChoices):
        BACK_END = "Back-end"
        FRONT_END = "Front-end"
        IOS = "IOS"
        ANDROID = "Android"

    description = models.fields.CharField(max_length=1000)
    type = models.fields.CharField(choices=Type.choices, max_length=10)


class Contributor(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='working')

    project = models.ForeignKey(to=Project, related_name='work_on')


class Issue(models.Model):

    class Priority(models.TextChoices):
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"

    class Balise(models.TextChoices):
        BUG = "Bug"
        FEATURE = "Feature"
        TASK = "Task"

    class Status(models.TextChoices):
        TO_DO = "To Do"
        IN_PROGRESS = "In Progress"
        FINISHED = "Finished"

    project = models.ForeignKey(to=Project)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    contributor = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)


class Comment(models.Model):
    issue = models.ForeignKey(to=Issue)
