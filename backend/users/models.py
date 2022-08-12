from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Адрес электронной почты'
    )
    username = models.CharField(
        max_length=150, unique=True, verbose_name='Уникальный юзернейм'
    )
    first_name = models.CharField(
        max_length=150, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='follower', verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='following', verbose_name='Автор'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='stop_self_sub'
            )
        ]
