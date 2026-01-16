"""Base DTO classes."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PaginatedDTO:
    """Paginated response DTO."""
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
