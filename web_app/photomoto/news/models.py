from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import CustomerUser

class Posts(models.Model):
    title = models.CharField('Название', max_length=50, default = "")
    annons = models.CharField('Анносы', max_length=250, default = "")
    photo = models.ImageField(blank = True,upload_to = 'images' )
    author = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title 
        
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

# Create your models here.


