"""
Products Module — Repository
================================
Database access layer for products and catalog.
"""

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.products.models import (
    Brand, Category, Collection, FragranceFamily, Note,
    Product, ProductImage, ProductNote, ProductVariant, PriceHistory,
)
from src.modules.products.schemas import ProductFilter


class ProductRepository:
    """Repository for product database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Product CRUD ─────────────────────────────────────────────────────

    async def get_by_id(self, product_id: int) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.brand),
                selectinload(Product.fragrance_family),
                selectinload(Product.categories),
                selectinload(Product.collections),
                selectinload(Product.variants),
                selectinload(Product.images),
                selectinload(Product.product_notes).selectinload(ProductNote.note),
                selectinload(Product.price_history),
            )
            .where(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Product | None:
        stmt = (
            select(Product)
            .options(
                selectinload(Product.brand),
                selectinload(Product.fragrance_family),
                selectinload(Product.categories),
                selectinload(Product.collections),
                selectinload(Product.variants),
                selectinload(Product.images),
                selectinload(Product.product_notes).selectinload(ProductNote.note),
                selectinload(Product.price_history),
            )
            .where(Product.slug == slug)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many(
        self, filters: ProductFilter, offset: int = 0, limit: int = 20
    ) -> tuple[list[Product], int]:
        """Get paginated, filtered products."""
        base_stmt = select(Product)
        count_stmt = select(func.count(Product.id))

        # Apply filters
        conditions = []
        if filters.search:
            search = f"%{filters.search}%"
            conditions.append(
                or_(
                    Product.name.ilike(search),
                    Product.description.ilike(search),
                    Product.short_description.ilike(search),
                )
            )
        if filters.brand_id:
            conditions.append(Product.brand_id == filters.brand_id)
        if filters.fragrance_family_id:
            conditions.append(Product.fragrance_family_id == filters.fragrance_family_id)
        if filters.gender:
            conditions.append(Product.gender == filters.gender)
        if filters.concentration:
            conditions.append(Product.concentration == filters.concentration)
        if filters.min_price is not None:
            conditions.append(Product.base_price >= filters.min_price)
        if filters.max_price is not None:
            conditions.append(Product.base_price <= filters.max_price)
        if filters.min_rating is not None:
            conditions.append(Product.avg_rating >= filters.min_rating)
        if filters.is_featured is not None:
            conditions.append(Product.is_featured == filters.is_featured)
        if filters.is_best_seller is not None:
            conditions.append(Product.is_best_seller == filters.is_best_seller)
        if filters.is_new_arrival is not None:
            conditions.append(Product.is_new_arrival == filters.is_new_arrival)
        if filters.status:
            conditions.append(Product.status == filters.status)
        else:
            conditions.append(Product.status == "published")

        if conditions:
            base_stmt = base_stmt.where(and_(*conditions))
            count_stmt = count_stmt.where(and_(*conditions))

        # Sorting
        sort_column = getattr(Product, filters.sort_by, Product.created_at)
        if filters.sort_order == "asc":
            base_stmt = base_stmt.order_by(sort_column.asc())
        else:
            base_stmt = base_stmt.order_by(sort_column.desc())

        # Count
        total = (await self.db.execute(count_stmt)).scalar() or 0

        # Fetch with eager loading
        stmt = (
            base_stmt.options(
                selectinload(Product.brand),
                selectinload(Product.fragrance_family),
                selectinload(Product.images),
                selectinload(Product.variants),
            )
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.flush()
        return await self.get_by_id(product.id)  # type: ignore

    async def update(self, product: Product) -> Product:
        await self.db.flush()
        return await self.get_by_id(product.id)  # type: ignore

    async def delete(self, product: Product) -> None:
        product.status = "archived"
        await self.db.flush()

    async def increment_view_count(self, product_id: int) -> None:
        from sqlalchemy import update
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(view_count=Product.view_count + 1)
        )
        await self.db.execute(stmt)

    # ── Brand CRUD ───────────────────────────────────────────────────────

    async def get_all_brands(self, active_only: bool = True) -> list[Brand]:
        stmt = select(Brand).order_by(Brand.name)
        if active_only:
            stmt = stmt.where(Brand.is_active == True)  # noqa: E712
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_brand_by_id(self, brand_id: int) -> Brand | None:
        result = await self.db.execute(select(Brand).where(Brand.id == brand_id))
        return result.scalar_one_or_none()

    async def create_brand(self, brand: Brand) -> Brand:
        self.db.add(brand)
        await self.db.flush()
        return brand

    async def update_brand(self, brand: Brand) -> Brand:
        await self.db.flush()
        return brand

    # ── Category CRUD ────────────────────────────────────────────────────

    async def get_all_categories(self, active_only: bool = True) -> list[Category]:
        stmt = select(Category).order_by(Category.sort_order, Category.name)
        if active_only:
            stmt = stmt.where(Category.is_active == True)  # noqa: E712
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_category_by_id(self, category_id: int) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def create_category(self, category: Category) -> Category:
        self.db.add(category)
        await self.db.flush()
        return category

    # ── Collection CRUD ──────────────────────────────────────────────────

    async def get_all_collections(self, active_only: bool = True) -> list[Collection]:
        stmt = select(Collection).order_by(Collection.sort_order, Collection.name)
        if active_only:
            stmt = stmt.where(Collection.is_active == True)  # noqa: E712
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_featured_collections(self) -> list[Collection]:
        stmt = (
            select(Collection)
            .where(Collection.is_featured == True, Collection.is_active == True)  # noqa: E712
            .order_by(Collection.sort_order)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_collection(self, collection: Collection) -> Collection:
        self.db.add(collection)
        await self.db.flush()
        return collection

    # ── Fragrance Families ───────────────────────────────────────────────

    async def get_all_fragrance_families(self) -> list[FragranceFamily]:
        result = await self.db.execute(select(FragranceFamily).order_by(FragranceFamily.name))
        return list(result.scalars().all())

    # ── Notes ────────────────────────────────────────────────────────────

    async def get_all_notes(self) -> list[Note]:
        result = await self.db.execute(select(Note).order_by(Note.name))
        return list(result.scalars().all())

    # ── Statistics ───────────────────────────────────────────────────────

    async def count_products(self, status: str | None = None) -> int:
        stmt = select(func.count(Product.id))
        if status:
            stmt = stmt.where(Product.status == status)
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_top_products(self, limit: int = 10) -> list[Product]:
        stmt = (
            select(Product)
            .options(selectinload(Product.brand), selectinload(Product.images))
            .where(Product.status == "published")
            .order_by(Product.total_sold.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_low_stock_variants(self, threshold: int = 10) -> list[ProductVariant]:
        stmt = (
            select(ProductVariant)
            .options(selectinload(ProductVariant.product).selectinload(Product.brand))
            .where(ProductVariant.stock_quantity <= threshold, ProductVariant.is_active == True)  # noqa: E712
            .order_by(ProductVariant.stock_quantity.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
