"""
Orders Module — SQLAlchemy Models
====================================
Order, OrderItem, and OrderTimeline models.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Order(Base):
    """Customer order."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(30), default="pending"
    )  # pending, confirmed, processing, shipped, delivered, cancelled, refunded

    # Amounts
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    tax_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Shipping
    shipping_address: Mapped[str | None] = mapped_column(Text)  # JSON string
    billing_address: Mapped[str | None] = mapped_column(Text)  # JSON string
    shipping_method: Mapped[str | None] = mapped_column(String(50))
    tracking_number: Mapped[str | None] = mapped_column(String(100))

    # Payment
    payment_method: Mapped[str | None] = mapped_column(String(50))
    payment_status: Mapped[str] = mapped_column(String(30), default="pending")

    # Coupon
    coupon_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("coupons.id", ondelete="SET NULL")
    )
    coupon_code: Mapped[str | None] = mapped_column(String(50))

    # Notes
    customer_note: Mapped[str | None] = mapped_column(Text)
    admin_note: Mapped[str | None] = mapped_column(Text)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
    timeline: Mapped[list["OrderTimeline"]] = relationship(
        back_populates="order", cascade="all, delete-orphan", order_by="OrderTimeline.created_at"
    )
    coupon: Mapped["Coupon | None"] = relationship()

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)


class OrderItem(Base):
    """Individual item in an order."""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    variant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True
    )
    product_name: Mapped[str] = mapped_column(String(300), nullable=False)
    variant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    product_image: Mapped[str | None] = mapped_column(String(500))

    order: Mapped["Order"] = relationship(back_populates="items")
    variant: Mapped["ProductVariant | None"] = relationship(back_populates="order_items")


class OrderTimeline(Base):
    """Order status timeline / activity log."""

    __tablename__ = "order_timeline"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    order: Mapped["Order"] = relationship(back_populates="timeline")


# Forward references
from src.modules.auth.models import User  # noqa: E402, F401
from src.modules.products.models import ProductVariant  # noqa: E402, F401
from src.modules.discounts.models import Coupon  # noqa: E402, F401
