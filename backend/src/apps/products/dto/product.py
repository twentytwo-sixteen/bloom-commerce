"""Product DTOs."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ProductImageDTO:
    """Фото товара."""
    id: int
    url: str
    alt_text: str
    is_main: bool
    sort_order: int


@dataclass(frozen=True, slots=True)
class ProductListDTO:
    """Товар для списка/каталога (минимум данных)."""
    id: int
    title: str
    slug: str
    price: int  # копейки
    old_price: int | None
    is_available: bool
    main_image_url: str | None
    category_slug: str


@dataclass(frozen=True)
class ProductDetailDTO:
    """Полная информация о товаре."""
    id: int
    title: str
    slug: str
    description: str
    price: int  # копейки
    old_price: int | None
    qty_available: int
    is_unlimited: bool
    is_available: bool
    category_id: int
    category_title: str
    category_slug: str
    images: list[ProductImageDTO] = field(default_factory=list)
    created_at: datetime | None = None


# === Input DTOs ===

@dataclass(slots=True)
class ProductCreateDTO:
    """Данные для создания товара."""
    category_id: int
    title: str
    description: str = ''
    price: int = 0
    old_price: int | None = None
    qty_available: int = 0
    is_unlimited: bool = False
    is_active: bool = True
    sort_order: int = 0


@dataclass(slots=True)
class ProductUpdateDTO:
    """Данные для обновления товара."""
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    old_price: int | None = None
    qty_available: int | None = None
    is_unlimited: bool | None = None
    is_active: bool | None = None
    sort_order: int | None = None
