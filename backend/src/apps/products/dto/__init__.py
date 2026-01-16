"""Products DTOs."""
from apps.products.dto.category import CategoryDTO, CategoryDetailDTO
from apps.products.dto.product import (
    ProductCreateDTO,
    ProductDetailDTO,
    ProductImageDTO,
    ProductListDTO,
    ProductUpdateDTO,
)

__all__ = [
    # Category
    'CategoryDTO',
    'CategoryDetailDTO',
    # Product
    'ProductListDTO',
    'ProductDetailDTO',
    'ProductImageDTO',
    'ProductCreateDTO',
    'ProductUpdateDTO',
]
