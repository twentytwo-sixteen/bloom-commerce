"""Product model."""
from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Product(TimeStampedModel):
    """
    Товар (букет/композиция).

    MVP-версия: цена и наличие прямо в модели.
    Варианты (размеры) добавим когда понадобится.
    """

    category = models.ForeignKey(
        'products.Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name='URL-slug',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Состав, особенности, как ухаживать',
    )

    # === Цена (в копейках, чтобы избежать float-ошибок) ===
    price = models.PositiveIntegerField(
        verbose_name='Цена (копейки)',
        help_text='Цена в копейках. 150000 = 1500₽',
    )
    old_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Старая цена (копейки)',
        help_text='Для отображения скидки. Оставить пустым если нет скидки',
    )

    # === Наличие (упрощённо для MVP) ===
    qty_available = models.PositiveIntegerField(
        default=0,
        verbose_name='В наличии',
    )
    is_unlimited = models.BooleanField(
        default=False,
        verbose_name='Под заказ (неограничено)',
        help_text='Если True — товар всегда доступен',
    )

    # === Статус ===
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        db_index=True,
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_active', 'sort_order']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    # === Удобные свойства ===

    @property
    def price_display(self) -> str:
        """Цена для отображения: '1 500 ₽'"""
        return f"{self.price // 100:,}".replace(',', ' ') + ' ₽'

    @property
    def is_available(self) -> bool:
        """Можно ли купить прямо сейчас."""
        return self.is_active and (self.is_unlimited or self.qty_available > 0)

    @property
    def has_discount(self) -> bool:
        """Есть ли скидка."""
        return self.old_price is not None and self.old_price > self.price
