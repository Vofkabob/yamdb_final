from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title
from users.models import User


class Review(models.Model):
    """
    Модель данных отзывов.
    """
    text = models.TextField(
        verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True)

    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews')

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ])

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews')

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
    """
    Модель данных комментариев.
    """
    text = models.TextField(
        verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True)

    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments')

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.author}, {self.pub_date}: {self.text}'
