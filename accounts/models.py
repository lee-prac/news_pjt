from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
