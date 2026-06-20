"""
PerfumeDecantBD — Pagination Utilities
========================================
Shared pagination response schemas and helpers.
"""

from math import ceil
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated API response."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: list[Any],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse":
        total_pages = ceil(total / page_size) if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )
