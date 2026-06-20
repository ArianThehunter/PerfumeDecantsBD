"""
Orders Module — Schemas, Service, Repository, Router
======================================================
Complete order management system.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ── Schemas ──────────────────────────────────────────────────────────────────


class OrderItemCreate(BaseModel):
    variant_id: int
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)
    shipping_address: str | None = None
    billing_address: str | None = None
    shipping_method: str | None = None
    payment_method: str | None = "cash_on_delivery"
    coupon_code: str | None = None
    customer_note: str | None = None


class OrderStatusUpdate(BaseModel):
    status: str
    note: str | None = None


class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    variant_name: str
    sku: str
    quantity: int
    unit_price: float
    total_price: float
    product_image: str | None = None

    model_config = {"from_attributes": True}


class OrderTimelineResponse(BaseModel):
    id: int
    status: str
    title: str
    description: str | None = None
    created_by: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int | None = None
    status: str
    subtotal: float
    shipping_cost: float
    tax_amount: float
    discount_amount: float
    total: float
    shipping_method: str | None = None
    tracking_number: str | None = None
    payment_method: str | None = None
    payment_status: str
    coupon_code: str | None = None
    customer_note: str | None = None
    created_at: datetime
    updated_at: datetime
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    items: list[OrderItemResponse] = []
    timeline: list[OrderTimelineResponse] = []

    model_config = {"from_attributes": True}

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)


class OrderListResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total: float
    payment_status: str
    created_at: datetime
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}
