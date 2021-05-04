from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
     first_name = models.CharField(max_length=200)
     last_name = models.CharField(max_length=200)
     email = models.CharField(max_length=200, unique=True)
     password = models.CharField(max_length=200)
     username = None

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

