from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings 

class CustomerUser(AbstractUser):
    age = models.IntegerField(null =True, blank = True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    resume_city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    resume_genres = models.CharField(max_length=200, blank=True, null=True, verbose_name="Жанры съемки")
    def __str__(self):
        return self.username

class Portfolio(models.Model):
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Портфолио {self.user.username}"

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Фото {self.id}"
    
class Photo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='portfolio_photos/', verbose_name='Фото')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f'Фото пользователя {self.user.username} от {self.uploaded_at}'
    
class PortfolioPhoto(models.Model):
    GENRE_CHOICES = [
        ('portrait', 'Портрет'),
        ('landscape', 'Пейзаж'),
        ('interior', 'Интерьер'),
        ('reportage', 'Репортаж'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio_photos'
    )

    image = models.ImageField(upload_to='portfolio_photos/')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='portrait')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.user.username} - {self.get_genre_display()}'