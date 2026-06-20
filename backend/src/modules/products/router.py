"""
Products Module — API Router
================================
Product catalog, brand, category, and collection endpoints.
"""

from fastapi import APIRouter, Depends, Query

from src.core.dependencies import CurrentUser, DbSession, Pagination, OptionalUser, require_role
from src.core.pagination import PaginatedResponse
from src.modules.products.repository import ProductRepository
from src.modules.products.schemas import (
    BrandCreate, BrandResponse, BrandUpdate,
    CategoryCreate, CategoryResponse, CategoryUpdate,
    CollectionCreate, CollectionResponse, CollectionUpdate,
    FragranceFamilyResponse, NoteResponse,
    ProductCreate, ProductDetailResponse, ProductFilter,
    ProductListResponse, ProductUpdate,
)
from src.modules.products.service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])
brands_router = APIRouter(prefix="/brands", tags=["Brands"])
categories_router = APIRouter(prefix="/categories", tags=["Categories"])
collections_router = APIRouter(prefix="/collections", tags=["Collections"])


def get_service(db: DbSession) -> ProductService:
    return ProductService(ProductRepository(db))


# ── Product Endpoints ────────────────────────────────────────────────────────


@router.get("", response_model=PaginatedResponse[ProductListResponse])
async def list_products(
    pagination: Pagination,
    search: str | None = None,
    brand_id: int | None = None,
    category_id: int | None = None,
    gender: str | None = None,
    concentration: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_rating: float | None = None,
    in_stock: bool | None = None,
    is_featured: bool | None = None,
    is_best_seller: bool | None = None,
    sort_by: str = Query("created_at", pattern="^(created_at|base_price|avg_rating|total_sold|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    service: ProductService = Depends(get_service),
):
    """List products with filtering and pagination."""
    filters = ProductFilter(
        search=search,
        brand_id=brand_id,
        category_id=category_id,
        gender=gender,
        concentration=concentration,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock=in_stock,
        is_featured=is_featured,
        is_best_seller=is_best_seller,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    products, total = await service.list_products(
        filters, pagination.page, pagination.page_size
    )
    return PaginatedResponse.create(products, total, pagination.page, pagination.page_size)


@router.get("/featured", response_model=list[ProductListResponse])
async def get_featured_products(
    limit: int = Query(8, ge=1, le=50),
    service: ProductService = Depends(get_service),
):
    """Get featured products for homepage."""
    filters = ProductFilter(is_featured=True)
    products, _ = await service.list_products(filters, 1, limit)
    return products


@router.get("/best-sellers", response_model=list[ProductListResponse])
async def get_best_sellers(
    limit: int = Query(8, ge=1, le=50),
    service: ProductService = Depends(get_service),
):
    """Get best-selling products."""
    filters = ProductFilter(is_best_seller=True, sort_by="total_sold")
    products, _ = await service.list_products(filters, 1, limit)
    return products


@router.get("/new-arrivals", response_model=list[ProductListResponse])
async def get_new_arrivals(
    limit: int = Query(8, ge=1, le=50),
    service: ProductService = Depends(get_service),
):
    """Get new arrival products."""
    filters = ProductFilter(is_new_arrival=True, sort_by="created_at")
    products, _ = await service.list_products(filters, 1, limit)
    return products


@router.get("/{slug}", response_model=ProductDetailResponse)
async def get_product(slug: str, service: ProductService = Depends(get_service)):
    """Get full product details by slug."""
    return await service.get_product_by_slug(slug)


@router.post(
    "",
    response_model=ProductDetailResponse,
    status_code=201,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def create_product(
    data: ProductCreate, service: ProductService = Depends(get_service)
):
    """Create a new product (admin)."""
    return await service.create_product(data)


@router.put(
    "/{product_id}",
    response_model=ProductDetailResponse,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(get_service),
):
    """Update a product (admin)."""
    return await service.update_product(product_id, data)


@router.delete(
    "/{product_id}",
    status_code=204,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def delete_product(
    product_id: int, service: ProductService = Depends(get_service)
):
    """Soft-delete a product (admin)."""
    await service.delete_product(product_id)


# ── Brand Endpoints ──────────────────────────────────────────────────────────


@brands_router.get("", response_model=list[BrandResponse])
async def list_brands(service: ProductService = Depends(get_service)):
    """Get all active brands."""
    return await service.get_brands()


@brands_router.post(
    "",
    response_model=BrandResponse,
    status_code=201,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def create_brand(
    data: BrandCreate, service: ProductService = Depends(get_service)
):
    return await service.create_brand(data)


@brands_router.put(
    "/{brand_id}",
    response_model=BrandResponse,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def update_brand(
    brand_id: int, data: BrandUpdate, service: ProductService = Depends(get_service)
):
    return await service.update_brand(brand_id, data)


# ── Category Endpoints ───────────────────────────────────────────────────────


@categories_router.get("", response_model=list[CategoryResponse])
async def list_categories(service: ProductService = Depends(get_service)):
    """Get all active categories."""
    return await service.get_categories()


@categories_router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def create_category(
    data: CategoryCreate, service: ProductService = Depends(get_service)
):
    return await service.create_category(data)


# ── Collection Endpoints ─────────────────────────────────────────────────────


@collections_router.get("", response_model=list[CollectionResponse])
async def list_collections(service: ProductService = Depends(get_service)):
    """Get all active collections."""
    return await service.get_collections()


@collections_router.get("/featured", response_model=list[CollectionResponse])
async def get_featured_collections(service: ProductService = Depends(get_service)):
    """Get featured collections for homepage."""
    return await service.get_featured_collections()


@collections_router.post(
    "",
    response_model=CollectionResponse,
    status_code=201,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def create_collection(
    data: CollectionCreate, service: ProductService = Depends(get_service)
):
    return await service.create_collection(data)


# ── Utility Endpoints ────────────────────────────────────────────────────────


@router.get("/meta/fragrance-families", response_model=list[FragranceFamilyResponse])
async def get_fragrance_families(service: ProductService = Depends(get_service)):
    """Get all fragrance families for filters."""
    return await service.repo.get_all_fragrance_families()


@router.get("/meta/notes", response_model=list[NoteResponse])
async def get_notes(service: ProductService = Depends(get_service)):
    """Get all fragrance notes."""
    return await service.repo.get_all_notes()
