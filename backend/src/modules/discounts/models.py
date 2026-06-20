"""
Discounts Module — Models & Router
======================================
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.dependencies import DbSession, Pagination, require_role
from src.core.exceptions import NotFoundException, ValidationException
from src.core.pagination import PaginatedResponse


# ── Models ───────────────────────────────────────────────────────────────────


class Coupon(Base):
    """Discount coupon."""

    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False)  # percentage, fixed
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    min_order_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    max_discount_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    usage_limit: Mapped[int | None] = mapped_column(Integer)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    usages: Mapped[list["CouponUsage"]] = relationship(back_populates="coupon")

    @property
    def is_valid(self) -> bool:
        now = datetime.now(UTC)
        if not self.is_active:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True


class CouponUsage(Base):
    """Track coupon usage."""

    __tablename__ = "coupon_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    coupon_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("coupons.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    order_id: Mapped[int | None] = mapped_column(Integer)
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    coupon: Mapped["Coupon"] = relationship(back_populates="usages")


class Campaign(Base):
    """Marketing campaign."""

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    campaign_type: Mapped[str] = mapped_column(String(50))  # flash_sale, bundle, seasonal
    discount_percentage: Mapped[float | None] = mapped_column(Numeric(5, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


# ── Schemas ──────────────────────────────────────────────────────────────────


class CouponCreate(BaseModel):
    code: str = Field(max_length=50)
    description: str | None = None
    discount_type: str = Field(pattern="^(percentage|fixed)$")
    discount_value: float = Field(gt=0)
    min_order_amount: float | None = None
    max_discount_amount: float | None = None
    usage_limit: int | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None


class CouponResponse(BaseModel):
    id: int
    code: str
    description: str | None = None
    discount_type: str
    discount_value: float
    min_order_amount: float | None = None
    max_discount_amount: float | None = None
    usage_limit: int | None = None
    usage_count: int = 0
    is_active: bool
    starts_at: datetime | None = None
    expires_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CouponValidateResponse(BaseModel):
    valid: bool
    discount_amount: float = 0
    message: str


# ── Router ───────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/discounts", tags=["Discounts"])


@router.get(
    "/coupons",
    response_model=PaginatedResponse[CouponResponse],
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def list_coupons(pagination: Pagination, db: DbSession):
    """List all coupons (admin)."""
    count = (await db.execute(select(func.count(Coupon.id)))).scalar() or 0
    stmt = (
        select(Coupon)
        .order_by(Coupon.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.page_size)
    )
    result = await db.execute(stmt)
    return PaginatedResponse.create(
        list(result.scalars().all()), count, pagination.page, pagination.page_size
    )


@router.post(
    "/coupons",
    response_model=CouponResponse,
    status_code=201,
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def create_coupon(data: CouponCreate, db: DbSession):
    """Create a discount coupon (admin)."""
    # Check uniqueness
    existing = await db.execute(select(Coupon).where(Coupon.code == data.code.upper()))
    if existing.scalar_one_or_none():
        raise ValidationException(f"Coupon code '{data.code}' already exists")

    coupon = Coupon(**data.model_dump())
    coupon.code = coupon.code.upper()
    db.add(coupon)
    await db.flush()
    return coupon


@router.post("/coupons/validate", response_model=CouponValidateResponse)
async def validate_coupon(code: str, order_total: float, db: DbSession):
    """Validate a coupon code."""
    stmt = select(Coupon).where(Coupon.code == code.upper())
    result = await db.execute(stmt)
    coupon = result.scalar_one_or_none()

    if not coupon:
        return CouponValidateResponse(valid=False, message="Invalid coupon code")

    if not coupon.is_valid:
        return CouponValidateResponse(valid=False, message="Coupon has expired or reached usage limit")

    if coupon.min_order_amount and order_total < float(coupon.min_order_amount):
        return CouponValidateResponse(
            valid=False,
            message=f"Minimum order amount is {coupon.min_order_amount}",
        )

    # Calculate discount
    if coupon.discount_type == "percentage":
        discount = order_total * float(coupon.discount_value) / 100
        if coupon.max_discount_amount:
            discount = min(discount, float(coupon.max_discount_amount))
    else:
        discount = float(coupon.discount_value)

    return CouponValidateResponse(
        valid=True, discount_amount=discount, message="Coupon applied successfully"
    )
