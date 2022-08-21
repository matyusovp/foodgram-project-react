from django.core.validators import MinValueValidator
from django.db import models

from users.models import UserProfile


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=150, verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name='Название'
    )
    color = models.CharField(
        verbose_name='Цвет в HEX', unique=True, max_length=7
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='автор рецепта'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Список ингредиентов'
    )
    name = models.CharField(max_length=200, verbose_name='Название')

    image = models.ImageField(
        upload_to='recipes/', verbose_name='Картинка, закодированная в Base64'
    )
    text = models.TextField(max_length=200, verbose_name='Описание')

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1, message='Время должно быть больше 1 минуты'
            )
        ]
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='shoppinglist', verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shoppinglist', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='1unique user-recipe'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='2unique user-recipe'
            )
        ]


class IngredientQnt(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1,
                              message='Количество должно быть больше 1 штуки!')
        ]
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingr-recipe'
            )
        ]
