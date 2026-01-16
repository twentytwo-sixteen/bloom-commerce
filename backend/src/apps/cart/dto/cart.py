"""Cart DTOs."""
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CartItemDTO:
    """Позиция в корзине."""
    product_id: int
    product_title: str
    product_slug: str
    price: int  # копейки
    qty: int
    line_total: int  # price * qty
    image_url: str | None
    is_available: bool
    max_qty: int | None  # None если unlimited


@dataclass(frozen=True)
class CartDTO:
    """Корзина целиком."""
    items: list[CartItemDTO] = field(default_factory=list)
    subtotal: int = 0  # сумма всех позиций (копейки)
    items_count: int = 0  # количество уникальных товаров
    total_qty: int = 0  # общее количество штук


# === Input DTOs ===

@dataclass(slots=True)
class CartItemAddDTO:
    """Добавление товара в корзину."""
    product_id: int
    qty: int = 1


@dataclass(slots=True)
class CartItemUpdateDTO:
    """Обновление количества в корзине."""
    product_id: int
    qty: int
