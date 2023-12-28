from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, null=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    company = models.CharField(max_length=150)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'password', 'email', 'surname', 'company', 'username']


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Services(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='service_image')
    url = models.CharField(max_length=150)
