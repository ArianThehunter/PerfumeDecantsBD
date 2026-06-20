"""
Products Module — Service Layer
===================================
Business logic for product management.
"""

import re

from src.core.exceptions import DuplicateException, NotFoundException
from src.modules.products.models import (
    Brand, Category, Collection, Product, ProductImage, ProductNote, ProductVariant,
)
from src.modules.products.repository import ProductRepository
from src.modules.products.schemas import (
    BrandCreate, BrandUpdate, CategoryCreate, CategoryUpdate,
    CollectionCreate, CollectionUpdate, ProductCreate, ProductFilter, ProductUpdate,
)


def slugify(text: str) -> str:
    """Generate a URL-friendly slug from text."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


class ProductService:
    """Service layer for product operations."""

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product", product_id)
        return product

    async def get_product_by_slug(self, slug: str) -> Product:
        product = await self.repo.get_by_slug(slug)
        if not product:
            raise NotFoundException("Product", slug)
        # Increment view count
        await self.repo.increment_view_count(product.id)
        return product

    async def list_products(
        self, filters: ProductFilter, page: int = 1, page_size: int = 20
    ) -> tuple[list[Product], int]:
        offset = (page - 1) * page_size
        return await self.repo.get_many(filters, offset, page_size)

    async def create_product(self, data: ProductCreate) -> Product:
        slug = data.slug or slugify(data.name)

        # Check slug uniqueness
        existing = await self.repo.get_by_slug(slug)
        if existing:
            slug = f"{slug}-{existing.id + 1}"

        product = Product(
            name=data.name,
            slug=slug,
            description=data.description,
            short_description=data.short_description,
            brand_id=data.brand_id,
            fragrance_family_id=data.fragrance_family_id,
            gender=data.gender,
            concentration=data.concentration,
            release_year=data.release_year,
            perfumer=data.perfumer,
            longevity_rating=data.longevity_rating,
            projection_rating=data.projection_rating,
            value_rating=data.value_rating,
            base_price=data.base_price,
            discount_price=data.discount_price,
            cost_price=data.cost_price,
            meta_title=data.meta_title,
            meta_description=data.meta_description,
            status=data.status,
            is_featured=data.is_featured,
            is_best_seller=data.is_best_seller,
            is_new_arrival=data.is_new_arrival,
            usage_occasion=data.usage_occasion,
            usage_season=data.usage_season,
            sku=data.sku,
            barcode=data.barcode,
        )

        product = await self.repo.create(product)

        # Add variants
        for v in data.variants:
            variant = ProductVariant(product_id=product.id, **v.model_dump())
            self.repo.db.add(variant)

        # Add notes
        for n in data.notes:
            note = ProductNote(
                product_id=product.id, note_id=n.note_id, position=n.position
            )
            self.repo.db.add(note)

        await self.repo.db.flush()
        return await self.repo.get_by_id(product.id)  # type: ignore

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product", product_id)

        update_data = data.model_dump(exclude_unset=True, exclude={"category_ids", "collection_ids"})
        for field, value in update_data.items():
            setattr(product, field, value)

        return await self.repo.update(product)

    async def delete_product(self, product_id: int) -> None:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product", product_id)
        await self.repo.delete(product)

    # ── Brands ───────────────────────────────────────────────────────────

    async def get_brands(self) -> list[Brand]:
        return await self.repo.get_all_brands()

    async def create_brand(self, data: BrandCreate) -> Brand:
        slug = data.slug or slugify(data.name)
        brand = Brand(slug=slug, **data.model_dump(exclude={"slug"}))
        return await self.repo.create_brand(brand)

    async def update_brand(self, brand_id: int, data: BrandUpdate) -> Brand:
        brand = await self.repo.get_brand_by_id(brand_id)
        if not brand:
            raise NotFoundException("Brand", brand_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(brand, field, value)
        return await self.repo.update_brand(brand)

    # ── Categories ───────────────────────────────────────────────────────

    async def get_categories(self) -> list[Category]:
        return await self.repo.get_all_categories()

    async def create_category(self, data: CategoryCreate) -> Category:
        slug = data.slug or slugify(data.name)
        category = Category(slug=slug, **data.model_dump(exclude={"slug"}))
        return await self.repo.create_category(category)

    # ── Collections ──────────────────────────────────────────────────────

    async def get_collections(self) -> list[Collection]:
        return await self.repo.get_all_collections()

    async def get_featured_collections(self) -> list[Collection]:
        return await self.repo.get_featured_collections()

    async def create_collection(self, data: CollectionCreate) -> Collection:
        slug = data.slug or slugify(data.name)
        collection = Collection(slug=slug, **data.model_dump(exclude={"slug"}))
        return await self.repo.create_collection(collection)

    # ── Dashboard Data ───────────────────────────────────────────────────

    async def get_top_products(self, limit: int = 10) -> list[Product]:
        return await self.repo.get_top_products(limit)

    async def get_low_stock(self, threshold: int = 10) -> list[ProductVariant]:
        return await self.repo.get_low_stock_variants(threshold)
