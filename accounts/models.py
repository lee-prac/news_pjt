from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    gender_choices = [("m", "남성"), ("f", "여성")]
    
    nickname = models.CharField(max_length=50)
    birth = models.DateField()
    
    gender =models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    
    
    introduction = models.TextField(default="")
    