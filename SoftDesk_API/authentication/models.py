from django.db import models
from django.contrib.auth.models import AbstractUser

class USer(AbstractUser):
    birthdate = models.DateTimeField(auto_now_add=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)