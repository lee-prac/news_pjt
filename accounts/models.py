from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    username = None
    user_id = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_id