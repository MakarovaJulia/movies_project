from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MovieGenre(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    genres = models.ManyToManyField(MovieGenre, verbose_name='Жанры', blank=True)
    image = models.ImageField(upload_to='movies/', null=True, blank=True, verbose_name='Картинка')
