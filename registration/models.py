from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=255, verbose_name='Telefonnummer (frivilligt)', blank=True, null=True)