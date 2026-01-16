"""Products views."""
from apps.products.views.category import CategoryViewSet
from apps.products.views.product import ProductViewSet

__all__ = [
    'CategoryViewSet',
    'ProductViewSet',
]
