"""
Reviews Module — Models & Router
===================================
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Float, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.core.database import Base
from src.core.dependencies import CurrentUser, DbSession, Pagination, require_role
from src.core.exceptions import NotFoundException
from src.core.pagination import PaginatedResponse


# ── Models ───────────────────────────────────────────────────────────────────


class Review(Base):
    """Product review from a customer."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    title: Mapped[str | None] = mapped_column(String(200))
    content: Mapped[str | None] = mapped_column(Text)
    is_verified_purchase: Mapped[bool] = mapped_column(Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    admin_reply: Mapped[str | None] = mapped_column(Text)
    admin_reply_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    product: Mapped["Product"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")


# ── Schemas ──────────────────────────────────────────────────────────────────


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    title: str | None = Field(None, max_length=200)
    content: str | None = None


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    title: str | None = None
    content: str | None = None
    is_verified_purchase: bool = False
    is_approved: bool = False
    is_featured: bool = False
    helpful_count: int = 0
    admin_reply: str | None = None
    admin_reply_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewReply(BaseModel):
    reply: str


class ReviewModeration(BaseModel):
    is_approved: bool
    is_featured: bool = False


# ── Router ───────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/product/{product_id}", response_model=PaginatedResponse[ReviewResponse])
async def get_product_reviews(
    product_id: int, pagination: Pagination, db: DbSession
):
    """Get approved reviews for a product."""
    count_stmt = select(func.count(Review.id)).where(
        Review.product_id == product_id, Review.is_approved == True  # noqa: E712
    )
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(Review)
        .where(Review.product_id == product_id, Review.is_approved == True)  # noqa: E712
        .order_by(Review.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.page_size)
    )
    result = await db.execute(stmt)
    reviews = list(result.scalars().all())
    return PaginatedResponse.create(reviews, total, pagination.page, pagination.page_size)


@router.post("", response_model=ReviewResponse, status_code=201)
async def create_review(data: ReviewCreate, user: CurrentUser, db: DbSession):
    """Submit a product review."""
    review = Review(
        product_id=data.product_id,
        user_id=user.id,
        rating=data.rating,
        title=data.title,
        content=data.content,
    )
    db.add(review)
    await db.flush()
    return review


@router.get(
    "/pending",
    response_model=PaginatedResponse[ReviewResponse],
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def get_pending_reviews(pagination: Pagination, db: DbSession):
    """Get reviews awaiting moderation (admin)."""
    count_stmt = select(func.count(Review.id)).where(Review.is_approved == False)  # noqa: E712
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(Review)
        .where(Review.is_approved == False)  # noqa: E712
        .order_by(Review.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.page_size)
    )
    result = await db.execute(stmt)
    return PaginatedResponse.create(
        list(result.scalars().all()), total, pagination.page, pagination.page_size
    )


@router.put(
    "/{review_id}/moderate",
    response_model=ReviewResponse,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def moderate_review(review_id: int, data: ReviewModeration, db: DbSession):
    """Approve or reject a review (admin)."""
    review = await db.get(Review, review_id)
    if not review:
        raise NotFoundException("Review", review_id)
    review.is_approved = data.is_approved
    review.is_featured = data.is_featured
    await db.flush()

    # Update product avg rating
    if data.is_approved:
        from src.modules.products.models import Product
        stmt = select(func.avg(Review.rating)).where(
            Review.product_id == review.product_id, Review.is_approved == True  # noqa: E712
        )
        avg = (await db.execute(stmt)).scalar() or 0
        count_stmt = select(func.count(Review.id)).where(
            Review.product_id == review.product_id, Review.is_approved == True  # noqa: E712
        )
        count = (await db.execute(count_stmt)).scalar() or 0
        product = await db.get(Product, review.product_id)
        if product:
            product.avg_rating = float(avg)
            product.review_count = count

    return review


@router.put(
    "/{review_id}/reply",
    response_model=ReviewResponse,
    dependencies=[Depends(require_role("SuperAdmin", "Manager", "CustomerSupport"))],
)
async def reply_to_review(review_id: int, data: ReviewReply, db: DbSession):
    """Reply to a review (admin)."""
    review = await db.get(Review, review_id)
    if not review:
        raise NotFoundException("Review", review_id)
    review.admin_reply = data.reply
    review.admin_reply_at = datetime.now(UTC)
    await db.flush()
    return review


from src.modules.products.models import Product  # noqa: E402, F401
from src.modules.auth.models import User  # noqa: E402, F401
