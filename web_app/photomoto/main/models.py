from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings 
class CustomerUser(AbstractUser):
    age = models.IntegerField(null =True, blank = True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.username
