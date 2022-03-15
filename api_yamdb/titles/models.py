from django.db import models

from .validators import validate_year


class Category(models.Model):
    """
    Модель данных категорий.
    """
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256)
    slug = models.SlugField(
        verbose_name='Ключ',
        max_length=50,
        unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель данных жанров.
    """
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256)
    slug = models.SlugField(
        verbose_name='Ключ',
        max_length=50,
        unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель данных произведений.
    """
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        db_index=True)

    year = models.PositiveIntegerField(
        verbose_name='Год',
        validators=[validate_year])

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр')

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles')

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
