"""Category serializers."""
from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Категория для списка."""
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'sort_order',
            'products_count',
        ]
