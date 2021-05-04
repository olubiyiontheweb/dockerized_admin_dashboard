from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Permission(models.Model):
     name = models.CharField(max_length=200)


class Role(models.Model):
     name = models.CharField(max_length=200)
     permissions = models.ManyToManyField(Permission)

class User(AbstractBaseUser):
     first_name = models.CharField(max_length=200)
     last_name = models.CharField(max_length=200)
     email = models.CharField(max_length=200, unique=True)
     password = models.CharField(max_length=200)
     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
     username = None

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

