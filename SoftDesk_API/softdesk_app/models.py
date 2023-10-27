from django.db import models
from django.conf import settings


class Project(models.Model):

    class Type(models.TextChoices):
        BACK_END = "Back-end"
        FRONT_END = "Front-end"
        IOS = "IOS"
        ANDROID = "Android"

    name = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=1000)
    type = models.fields.CharField(choices=Type.choices, max_length=10)
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='authored_projects')


class Contributor(models.Model):

    class Role(models.TextChoices):
        CONTRIBUTOR = "Contributeur"
        AUTHOR = "Auteur"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='working')

    project = models.ForeignKey(to=Project, related_name='work_on',
                                on_delete=models.CASCADE, default=None)
    role = models.fields.CharField(choices=Role.choices, max_length=50, default='Contributeur')

    def is_author(self):
        if self.role == "Auteur":
            return True
        return False


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

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    priority = models.fields.CharField(choices=Priority.choices, max_length=10)
    balise = models.fields.CharField(choices=Balise.choices,  max_length=10)
    status = models.fields.CharField(choices=Status.choices,  max_length=15,
                                     default='To Do')
    time_created = models.DateTimeField(auto_now_add=True)
    contributor = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='contributed_issues')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='authored_issues')

    def in_progress(self):
        if self.status == "In Progress":
            return
        self.status = "In Progress"
        self.save()

    def finished(self):
        if self.status == "Finished":
            return
        self.status = "Finished"
        self.save()


class Comment(models.Model):
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='authored_Comments')
