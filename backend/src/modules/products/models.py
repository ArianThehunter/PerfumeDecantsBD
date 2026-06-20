"""
Products Module — SQLAlchemy Models
======================================
Product catalog with variants, images, notes, and relationships.
"""

from datetime import UTC, datetime

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer,
    Numeric, String, Table, Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


# ── Junction Tables ──────────────────────────────────────────────────────────

product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    ),
)

product_collections = Table(
    "product_collections",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "collection_id",
        Integer,
        ForeignKey("collections.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# ── Brand ────────────────────────────────────────────────────────────────────


class Brand(Base):
    """Perfume brand / house."""

    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    logo_url: Mapped[str | None] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(100))
    website: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    products: Mapped[list["Product"]] = relationship(back_populates="brand")


# ── Category ─────────────────────────────────────────────────────────────────


class Category(Base):
    """Product category with nested support."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL")
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    parent: Mapped["Category | None"] = relationship(
        back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    products: Mapped[list["Product"]] = relationship(
        secondary=product_categories, back_populates="categories"
    )


# ── Collection ───────────────────────────────────────────────────────────────


class Collection(Base):
    """Curated product collections (seasonal, featured, etc.)."""

    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    products: Mapped[list["Product"]] = relationship(
        secondary=product_collections, back_populates="collections"
    )


# ── Fragrance Note ───────────────────────────────────────────────────────────


class Note(Base):
    """Individual fragrance note (e.g., Bergamot, Jasmine, Musk)."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50))  # Citrus, Floral, Woody, etc.
    description: Mapped[str | None] = mapped_column(Text)
    icon: Mapped[str | None] = mapped_column(String(50))  # Emoji or icon identifier

    product_notes: Mapped[list["ProductNote"]] = relationship(back_populates="note")


# ── Fragrance Family ─────────────────────────────────────────────────────────


class FragranceFamily(Base):
    """Fragrance family classification (Floral, Oriental, Woody, Fresh)."""

    __tablename__ = "fragrance_families"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    color: Mapped[str | None] = mapped_column(String(7))  # Hex color

    products: Mapped[list["Product"]] = relationship(back_populates="fragrance_family")


# ── Product ──────────────────────────────────────────────────────────────────


class Product(Base):
    """Main product entity representing a perfume."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(300), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    short_description: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    brand_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    fragrance_family_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("fragrance_families.id", ondelete="SET NULL"), index=True
    )

    # Product attributes
    gender: Mapped[str] = mapped_column(String(20), default="Unisex")  # Men, Women, Unisex
    concentration: Mapped[str | None] = mapped_column(String(50))  # EDP, EDT, Parfum, etc.
    release_year: Mapped[int | None] = mapped_column(Integer)
    perfumer: Mapped[str | None] = mapped_column(String(200))

    # Performance ratings (1-10)
    longevity_rating: Mapped[float | None] = mapped_column(Float)
    projection_rating: Mapped[float | None] = mapped_column(Float)
    value_rating: Mapped[float | None] = mapped_column(Float)

    # Pricing
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    cost_price: Mapped[float | None] = mapped_column(Numeric(10, 2))

    # SEO
    meta_title: Mapped[str | None] = mapped_column(String(200))
    meta_description: Mapped[str | None] = mapped_column(String(500))

    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, published, archived
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_best_seller: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new_arrival: Mapped[bool] = mapped_column(Boolean, default=False)

    # Usage suggestions
    usage_occasion: Mapped[str | None] = mapped_column(String(200))  # Day, Night, Special
    usage_season: Mapped[str | None] = mapped_column(String(200))  # Spring, Summer, etc.

    # SKU / Barcode
    sku: Mapped[str | None] = mapped_column(String(50), unique=True, index=True)
    barcode: Mapped[str | None] = mapped_column(String(50))

    # Statistics
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    total_sold: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    brand: Mapped["Brand"] = relationship(back_populates="products")
    fragrance_family: Mapped["FragranceFamily | None"] = relationship(
        back_populates="products"
    )
    categories: Mapped[list["Category"]] = relationship(
        secondary=product_categories, back_populates="products"
    )
    collections: Mapped[list["Collection"]] = relationship(
        secondary=product_collections, back_populates="products"
    )
    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product", cascade="all, delete-orphan", order_by="ProductImage.sort_order"
    )
    product_notes: Mapped[list["ProductNote"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(back_populates="product")
    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    @property
    def current_price(self) -> float:
        return float(self.discount_price or self.base_price)

    @property
    def discount_percent(self) -> float | None:
        if self.discount_price and self.base_price:
            return round((1 - float(self.discount_price) / float(self.base_price)) * 100, 1)
        return None

    @property
    def total_stock(self) -> int:
        return sum(v.stock_quantity for v in self.variants)

    @property
    def in_stock(self) -> bool:
        return self.total_stock > 0


# ── Product Variant ──────────────────────────────────────────────────────────


class ProductVariant(Base):
    """Product size/concentration variant with own pricing and stock."""

    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "100ml EDP"
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    size_ml: Mapped[int | None] = mapped_column(Integer)  # Volume in ml
    concentration: Mapped[str | None] = mapped_column(String(50))

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    cost_price: Mapped[float | None] = mapped_column(Numeric(10, 2))

    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    safety_stock: Mapped[int] = mapped_column(Integer, default=5)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    barcode: Mapped[str | None] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    product: Mapped["Product"] = relationship(back_populates="variants")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="variant")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="variant")
    inventory_movements: Mapped[list["InventoryMovement"]] = relationship(
        back_populates="variant"
    )

    @property
    def is_low_stock(self) -> bool:
        return self.stock_quantity <= self.safety_stock

    @property
    def current_price(self) -> float:
        return float(self.discount_price or self.price)


# ── Product Image ────────────────────────────────────────────────────────────


class ProductImage(Base):
    """Product images with ordering support."""

    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    product: Mapped["Product"] = relationship(back_populates="images")


# ── Product Note ─────────────────────────────────────────────────────────────


class ProductNote(Base):
    """Links a note to a product with position (top, middle, base)."""

    __tablename__ = "product_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    note_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    position: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # top, middle, base

    product: Mapped["Product"] = relationship(back_populates="product_notes")
    note: Mapped["Note"] = relationship(back_populates="product_notes")


# ── Price History ────────────────────────────────────────────────────────────


class PriceHistory(Base):
    """Track price changes over time."""

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    old_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    new_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    product: Mapped["Product"] = relationship(back_populates="price_history")


# Forward references
from src.modules.orders.models import OrderItem  # noqa: E402, F401
from src.modules.cart.models import CartItem  # noqa: E402, F401
from src.modules.reviews.models import Review  # noqa: E402, F401
from src.modules.inventory.models import InventoryMovement  # noqa: E402, F401
