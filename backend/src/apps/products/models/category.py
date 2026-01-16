"""Category model."""
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    """
    Категория товаров.

    Простая структура для MVP. parent можно использовать позже
    для вложенных категорий.
    """

    title = models.CharField(
        max_length=120,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        verbose_name='URL-slug',
        help_text='Для красивых ссылок: /category/rozy',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки',
        db_index=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
