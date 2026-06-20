"""
Products Module — Pydantic Schemas
=====================================
Request/response schemas for product catalog endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, Field


# ── Nested Schemas ───────────────────────────────────────────────────────────


class BrandResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    logo_url: str | None = None
    country: str | None = None

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    parent_id: int | None = None
    sort_order: int = 0

    model_config = {"from_attributes": True}


class CollectionResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    is_featured: bool = False

    model_config = {"from_attributes": True}


class NoteResponse(BaseModel):
    id: int
    name: str
    category: str | None = None
    description: str | None = None
    icon: str | None = None

    model_config = {"from_attributes": True}


class ProductNoteResponse(BaseModel):
    position: str
    note: NoteResponse

    model_config = {"from_attributes": True}


class FragranceFamilyResponse(BaseModel):
    id: int
    name: str
    slug: str
    color: str | None = None

    model_config = {"from_attributes": True}


class ProductImageResponse(BaseModel):
    id: int
    url: str
    alt_text: str | None = None
    sort_order: int = 0
    is_primary: bool = False

    model_config = {"from_attributes": True}


class ProductVariantResponse(BaseModel):
    id: int
    name: str
    sku: str
    size_ml: int | None = None
    concentration: str | None = None
    price: float
    discount_price: float | None = None
    stock_quantity: int = 0
    safety_stock: int = 5
    is_active: bool = True

    model_config = {"from_attributes": True}

    @property
    def current_price(self) -> float:
        return self.discount_price or self.price


class PriceHistoryResponse(BaseModel):
    old_price: float
    new_price: float
    changed_at: datetime

    model_config = {"from_attributes": True}


# ── Product Response ─────────────────────────────────────────────────────────


class ProductListResponse(BaseModel):
    """Product in list/catalog views (lighter payload)."""

    id: int
    name: str
    slug: str
    short_description: str | None = None
    gender: str = "Unisex"
    concentration: str | None = None
    base_price: float
    discount_price: float | None = None
    status: str = "draft"
    is_featured: bool = False
    is_best_seller: bool = False
    is_new_arrival: bool = False
    avg_rating: float = 0.0
    review_count: int = 0
    total_sold: int = 0
    view_count: int = 0
    created_at: datetime

    brand: BrandResponse | None = None
    fragrance_family: FragranceFamilyResponse | None = None
    images: list[ProductImageResponse] = []
    variants: list[ProductVariantResponse] = []

    model_config = {"from_attributes": True}

    @property
    def primary_image(self) -> str | None:
        for img in self.images:
            if img.is_primary:
                return img.url
        return self.images[0].url if self.images else None

    @property
    def current_price(self) -> float:
        return self.discount_price or self.base_price


class ProductDetailResponse(ProductListResponse):
    """Full product detail with all relationships."""

    description: str | None = None
    release_year: int | None = None
    perfumer: str | None = None
    longevity_rating: float | None = None
    projection_rating: float | None = None
    value_rating: float | None = None
    cost_price: float | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    usage_occasion: str | None = None
    usage_season: str | None = None
    sku: str | None = None
    barcode: str | None = None
    published_at: datetime | None = None
    updated_at: datetime

    categories: list[CategoryResponse] = []
    collections: list[CollectionResponse] = []
    product_notes: list[ProductNoteResponse] = []
    price_history: list[PriceHistoryResponse] = []


# ── Request Schemas ──────────────────────────────────────────────────────────


class ProductVariantCreate(BaseModel):
    name: str = Field(max_length=100)
    sku: str = Field(max_length=50)
    size_ml: int | None = None
    concentration: str | None = None
    price: float = Field(gt=0)
    discount_price: float | None = None
    cost_price: float | None = None
    stock_quantity: int = Field(ge=0, default=0)
    safety_stock: int = Field(ge=0, default=5)
    barcode: str | None = None


class ProductNoteCreate(BaseModel):
    note_id: int
    position: str = Field(pattern="^(top|middle|base)$")


class ProductCreate(BaseModel):
    """Create a new product."""

    name: str = Field(max_length=300)
    slug: str | None = Field(None, max_length=300)
    description: str | None = None
    short_description: str | None = Field(None, max_length=500)

    brand_id: int
    fragrance_family_id: int | None = None
    gender: str = Field(default="Unisex", max_length=20)
    concentration: str | None = Field(None, max_length=50)
    release_year: int | None = None
    perfumer: str | None = Field(None, max_length=200)

    longevity_rating: float | None = Field(None, ge=0, le=10)
    projection_rating: float | None = Field(None, ge=0, le=10)
    value_rating: float | None = Field(None, ge=0, le=10)

    base_price: float = Field(gt=0)
    discount_price: float | None = None
    cost_price: float | None = None

    meta_title: str | None = Field(None, max_length=200)
    meta_description: str | None = Field(None, max_length=500)
    status: str = Field(default="draft")
    is_featured: bool = False
    is_best_seller: bool = False
    is_new_arrival: bool = False

    usage_occasion: str | None = None
    usage_season: str | None = None
    sku: str | None = None
    barcode: str | None = None

    category_ids: list[int] = []
    collection_ids: list[int] = []
    variants: list[ProductVariantCreate] = []
    notes: list[ProductNoteCreate] = []


class ProductUpdate(BaseModel):
    """Update product (all fields optional)."""

    name: str | None = None
    slug: str | None = None
    description: str | None = None
    short_description: str | None = None
    brand_id: int | None = None
    fragrance_family_id: int | None = None
    gender: str | None = None
    concentration: str | None = None
    release_year: int | None = None
    perfumer: str | None = None
    longevity_rating: float | None = None
    projection_rating: float | None = None
    value_rating: float | None = None
    base_price: float | None = None
    discount_price: float | None = None
    cost_price: float | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    status: str | None = None
    is_featured: bool | None = None
    is_best_seller: bool | None = None
    is_new_arrival: bool | None = None
    usage_occasion: str | None = None
    usage_season: str | None = None
    sku: str | None = None
    barcode: str | None = None
    category_ids: list[int] | None = None
    collection_ids: list[int] | None = None


class BrandCreate(BaseModel):
    name: str = Field(max_length=200)
    slug: str | None = None
    description: str | None = None
    logo_url: str | None = None
    country: str | None = None
    website: str | None = None


class BrandUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    logo_url: str | None = None
    country: str | None = None
    website: str | None = None


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    parent_id: int | None = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    parent_id: int | None = None
    sort_order: int | None = None


class CollectionCreate(BaseModel):
    name: str = Field(max_length=200)
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_featured: bool = False
    sort_order: int = 0


class CollectionUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_featured: bool | None = None
    sort_order: int | None = None


# ── Filter Schema ────────────────────────────────────────────────────────────


class ProductFilter(BaseModel):
    """Product search/filter parameters."""

    search: str | None = None
    brand_id: int | None = None
    category_id: int | None = None
    collection_id: int | None = None
    fragrance_family_id: int | None = None
    gender: str | None = None
    concentration: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_rating: float | None = None
    in_stock: bool | None = None
    is_featured: bool | None = None
    is_best_seller: bool | None = None
    is_new_arrival: bool | None = None
    status: str | None = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
