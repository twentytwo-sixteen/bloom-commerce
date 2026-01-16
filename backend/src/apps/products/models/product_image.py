"""ProductImage model."""
from django.db import models

from apps.core.models import TimeStampedModel


class ProductImage(TimeStampedModel):
    """
    Фотографии товара.
    
    Несколько фото на товар, одно главное для списка.
    """

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар',
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/',
        verbose_name='Изображение',
    )
    alt_text = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='Alt-текст',
        help_text='Для SEO и доступности',
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Главное фото',
        db_index=True,
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
    )

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['-is_main', 'sort_order']

    def __str__(self):
        return f"{self.product.title} - фото {self.pk}"

    def save(self, *args, **kwargs):
        # Если это главное фото — снимаем флаг с других
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product,
                is_main=True,
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
