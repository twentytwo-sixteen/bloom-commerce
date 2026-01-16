"""Category DTOs."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CategoryDTO:
    """Категория для списка/меню."""
    id: int
    title: str
    slug: str
    sort_order: int
    products_count: int | None = None


@dataclass(frozen=True, slots=True)
class CategoryDetailDTO:
    """Категория с полной информацией."""
    id: int
    title: str
    slug: str
    sort_order: int
    is_active: bool
    parent_id: int | None
    products_count: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
