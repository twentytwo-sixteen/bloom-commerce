"""Products admin with Unfold."""
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.decorators import display

from apps.products.models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Админка категорий."""
    list_display = ['title', 'slug', 'sort_order', 'show_status', 'show_products_count']
    list_filter = ['is_active']
    list_editable = ['sort_order']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['sort_order', 'title']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _products_count=Count('products', filter=models.Q(products__is_active=True))
        )

    @display(description='Статус', label={True: 'success', False: 'danger'})
    def show_status(self, obj):
        return obj.is_active, 'Активна' if obj.is_active else 'Скрыта'

    @display(description='Товаров')
    def show_products_count(self, obj):
        return obj._products_count


# Импорт для Q
from django.db import models


class ProductImageInline(TabularInline):
    """Инлайн фотографий товара."""
    model = ProductImage
    extra = 1
    fields = ['image', 'show_preview', 'is_main', 'sort_order', 'alt_text']
    readonly_fields = ['show_preview']
    tab = True

    @display(description='Превью')
    def show_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 100px; border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        return '—'


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Админка товаров."""
    list_display = [
        'show_image',
        'title',
        'category',
        'show_price',
        'show_stock',
        'show_availability',
        'show_status',
        'sort_order',
    ]
    list_display_links = ['show_image', 'title']
    list_filter = [
        'category',
        'is_active',
        'is_unlimited',
        ('created_at', RangeDateFilter),
    ]
    list_editable = ['sort_order']
    search_fields = ['title', 'slug', 'description']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category']
    inlines = [ProductImageInline]
    ordering = ['sort_order', '-created_at']
    list_per_page = 20

    fieldsets = (
        ('Основное', {
            'fields': ('category', 'title', 'slug', 'description'),
            'classes': ['tab'],
        }),
        ('Цена', {
            'fields': ('price', 'old_price'),
            'classes': ['tab'],
            'description': 'Цены указываются в копейках. 150000 = 1500₽',
        }),
        ('Наличие', {
            'fields': ('qty_available', 'is_unlimited'),
            'classes': ['tab'],
        }),
        ('Настройки', {
            'fields': ('is_active', 'sort_order'),
            'classes': ['tab'],
        }),
    )

    @display(description='')
    def show_image(self, obj):
        main = obj.images.filter(is_main=True).first() or obj.images.first()
        if main and main.image:
            return format_html(
                '<img src="{}" style="width: 48px; height: 48px; border-radius: 8px; object-fit: cover;" />',
                main.image.url
            )
        return format_html(
            '<div style="width: 48px; height: 48px; border-radius: 8px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; color: #9ca3af;">'
            '<span class="material-symbols-outlined" style="font-size: 24px;">image</span>'
            '</div>'
        )

    @display(description='Цена')
    def show_price(self, obj):
        price = f"{obj.price // 100:,}".replace(',', ' ') + ' ₽'
        if obj.old_price and obj.old_price > obj.price:
            discount = round((1 - obj.price / obj.old_price) * 100)
            return format_html(
                '<span style="font-weight: 600;">{}</span> '
                '<span style="background: #fef2f2; color: #dc2626; padding: 2px 6px; border-radius: 4px; font-size: 11px;">-{}%</span>',
                price, discount
            )
        return format_html('<span style="font-weight: 600;">{}</span>', price)

    @display(description='Остаток')
    def show_stock(self, obj):
        if obj.is_unlimited:
            return format_html(
                '<span style="color: #6366f1;">∞ Под заказ</span>'
            )
        if obj.qty_available == 0:
            return format_html(
                '<span style="color: #ef4444; font-weight: 600;">0</span>'
            )
        if obj.qty_available <= 5:
            return format_html(
                '<span style="color: #f59e0b; font-weight: 600;">{}</span>',
                obj.qty_available
            )
        return format_html(
            '<span style="color: #10b981; font-weight: 600;">{}</span>',
            obj.qty_available
        )

    @display(description='В наличии', label={True: 'success', False: 'danger'})
    def show_availability(self, obj):
        return obj.is_available, '✓' if obj.is_available else '✗'

    @display(description='Статус', label={True: 'success', False: 'warning'})
    def show_status(self, obj):
        return obj.is_active, 'Активен' if obj.is_active else 'Скрыт'


@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    """Админка фотографий (для массовых операций)."""
    list_display = ['id', 'show_preview', 'product', 'show_main', 'sort_order']
    list_filter = ['is_main', 'product__category']
    list_editable = ['sort_order']
    autocomplete_fields = ['product']
    list_per_page = 50

    @display(description='Фото')
    def show_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        return '—'

    @display(description='Главное', label={True: 'success', False: 'info'})
    def show_main(self, obj):
        return obj.is_main, '★ Главное' if obj.is_main else 'Доп.'
