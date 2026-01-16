"""Category views."""
from django.db import models
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.products.models import Category
from apps.products.serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Категории товаров.
    
    list: Список всех активных категорий
    retrieve: Детали категории по slug
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    pagination_class = None  # Категорий мало, пагинация не нужна

    def get_queryset(self):
        return (
            Category.objects
            .filter(is_active=True)
            .annotate(
                products_count=Count(
                    'products',
                    filter=models.Q(products__is_active=True)
                )
            )
            .order_by('sort_order', 'title')
        )
