"""Product serializers."""
from rest_framework import serializers

from apps.products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Фото товара."""
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'alt_text', 'is_main', 'sort_order']

    def get_url(self, obj) -> str:
        if obj.image:
            return obj.image.url
        return ''


class ProductListSerializer(serializers.ModelSerializer):
    """Товар для списка/каталога."""
    price_display = serializers.SerializerMethodField()
    old_price_display = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(read_only=True)
    main_image = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'price',
            'price_display',
            'old_price',
            'old_price_display',
            'has_discount',
            'is_available',
            'main_image',
            'category_slug',
        ]

    def get_price_display(self, obj) -> str:
        # \xa0 - неразрывный пробел, чтобы ₽ не переносился
        return f"{obj.price // 100:,}".replace(',', '\xa0') + '\xa0₽'

    def get_old_price_display(self, obj) -> str | None:
        if obj.old_price:
            return f"{obj.old_price // 100:,}".replace(',', '\xa0') + '\xa0₽'
        return None

    def get_has_discount(self, obj) -> bool:
        return obj.old_price is not None and obj.old_price > obj.price

    def get_main_image(self, obj) -> str | None:
        main = obj.images.filter(is_main=True).first()
        if main and main.image:
            return main.image.url
        # Fallback на первое фото
        first = obj.images.first()
        if first and first.image:
            return first.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Полная информация о товаре."""
    price_display = serializers.SerializerMethodField()
    old_price_display = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'price',
            'price_display',
            'old_price',
            'old_price_display',
            'has_discount',
            'qty_available',
            'is_unlimited',
            'is_available',
            'category',
            'images',
            'created_at',
        ]

    def get_price_display(self, obj) -> str:
        # \xa0 - неразрывный пробел, чтобы ₽ не переносился
        return f"{obj.price // 100:,}".replace(',', '\xa0') + '\xa0₽'

    def get_old_price_display(self, obj) -> str | None:
        if obj.old_price:
            return f"{obj.old_price // 100:,}".replace(',', '\xa0') + '\xa0₽'
        return None

    def get_has_discount(self, obj) -> bool:
        return obj.old_price is not None and obj.old_price > obj.price

    def get_category(self, obj) -> dict:
        return {
            'id': obj.category.id,
            'title': obj.category.title,
            'slug': obj.category.slug,
        }
