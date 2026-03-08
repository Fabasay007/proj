from django.db import models
class Posts(models.Model):
    title = models.CharField('Название', max_length=50, default = "")
    annons = models.CharField('Анносы', max_length=250, default = "")
    def __str__(self):
        
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
