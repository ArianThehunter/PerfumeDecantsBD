"""
Inventory Module — Models & Router
======================================
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.core.database import Base
from src.core.dependencies import DbSession, Pagination, require_role
from src.core.exceptions import NotFoundException
from src.core.pagination import PaginatedResponse


# ── Models ───────────────────────────────────────────────────────────────────


class Warehouse(Base):
    """Physical or logical warehouse."""

    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str | None] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    movements: Mapped[list["InventoryMovement"]] = relationship(back_populates="warehouse")


class InventoryMovement(Base):
    """Track stock movements (in/out)."""

    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    variant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_variants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    warehouse_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("warehouses.id", ondelete="SET NULL")
    )
    movement_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # purchase, sale, adjustment, return, transfer
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)  # Positive for in, negative for out
    reference: Mapped[str | None] = mapped_column(String(100))  # Order number or PO number
    notes: Mapped[str | None] = mapped_column(Text)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(10, 2))
    created_by: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    variant: Mapped["ProductVariant"] = relationship(back_populates="inventory_movements")
    warehouse: Mapped["Warehouse | None"] = relationship(back_populates="movements")


class Supplier(Base):
    """Product supplier."""

    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(back_populates="supplier")


class PurchaseOrder(Base):
    """Purchase order from supplier."""

    __tablename__ = "purchase_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    po_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    supplier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, ordered, received, cancelled
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    ordered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    supplier: Mapped["Supplier | None"] = relationship(back_populates="purchase_orders")
    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="purchase_order", cascade="all, delete-orphan"
    )


class PurchaseOrderItem(Base):
    """Item in a purchase order."""

    __tablename__ = "purchase_order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    purchase_order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False
    )
    variant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    purchase_order: Mapped["PurchaseOrder"] = relationship(back_populates="items")


# ── Schemas ──────────────────────────────────────────────────────────────────


class InventoryMovementResponse(BaseModel):
    id: int
    variant_id: int
    warehouse_id: int | None = None
    movement_type: str
    quantity: int
    reference: str | None = None
    notes: str | None = None
    unit_cost: float | None = None
    created_by: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class InventoryMovementCreate(BaseModel):
    variant_id: int
    warehouse_id: int | None = None
    movement_type: str
    quantity: int
    reference: str | None = None
    notes: str | None = None
    unit_cost: float | None = None


class InventorySummary(BaseModel):
    total_variants: int
    total_stock: int
    low_stock_count: int
    out_of_stock_count: int
    inventory_value: float


# ── Router ───────────────────────────────────────────────────────────────────

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    dependencies=[Depends(require_role("SuperAdmin", "Manager", "InventoryManager"))],
)


@router.get("/summary", response_model=InventorySummary)
async def get_inventory_summary(db: DbSession):
    """Get inventory summary stats."""
    from src.modules.products.models import ProductVariant

    total_variants = (
        await db.execute(select(func.count(ProductVariant.id)).where(ProductVariant.is_active == True))  # noqa: E712
    ).scalar() or 0

    total_stock = (
        await db.execute(select(func.sum(ProductVariant.stock_quantity)).where(ProductVariant.is_active == True))  # noqa: E712
    ).scalar() or 0

    low_stock = (
        await db.execute(
            select(func.count(ProductVariant.id)).where(
                ProductVariant.stock_quantity <= ProductVariant.safety_stock,
                ProductVariant.stock_quantity > 0,
                ProductVariant.is_active == True,  # noqa: E712
            )
        )
    ).scalar() or 0

    out_of_stock = (
        await db.execute(
            select(func.count(ProductVariant.id)).where(
                ProductVariant.stock_quantity == 0,
                ProductVariant.is_active == True,  # noqa: E712
            )
        )
    ).scalar() or 0

    # Inventory value = sum(stock * cost_price or price)
    value_result = await db.execute(
        select(
            func.sum(
                ProductVariant.stock_quantity * func.coalesce(
                    ProductVariant.cost_price, ProductVariant.price
                )
            )
        ).where(ProductVariant.is_active == True)  # noqa: E712
    )
    inventory_value = float(value_result.scalar() or 0)

    return InventorySummary(
        total_variants=total_variants,
        total_stock=total_stock,
        low_stock_count=low_stock,
        out_of_stock_count=out_of_stock,
        inventory_value=inventory_value,
    )


@router.get("/movements", response_model=PaginatedResponse[InventoryMovementResponse])
async def get_movements(
    pagination: Pagination,
    variant_id: int | None = None,
    movement_type: str | None = None,
    db: DbSession = None,
):
    """Get inventory movement history."""
    conditions = []
    if variant_id:
        conditions.append(InventoryMovement.variant_id == variant_id)
    if movement_type:
        conditions.append(InventoryMovement.movement_type == movement_type)

    count_stmt = select(func.count(InventoryMovement.id))
    stmt = select(InventoryMovement)

    if conditions:
        from sqlalchemy import and_
        count_stmt = count_stmt.where(and_(*conditions))
        stmt = stmt.where(and_(*conditions))

    total = (await db.execute(count_stmt)).scalar() or 0
    stmt = stmt.order_by(InventoryMovement.created_at.desc()).offset(pagination.offset).limit(pagination.page_size)
    result = await db.execute(stmt)
    return PaginatedResponse.create(
        list(result.scalars().all()), total, pagination.page, pagination.page_size
    )


@router.post("/movements", response_model=InventoryMovementResponse, status_code=201)
async def create_movement(data: InventoryMovementCreate, db: DbSession):
    """Record an inventory movement."""
    from src.modules.products.models import ProductVariant

    variant = await db.get(ProductVariant, data.variant_id)
    if not variant:
        raise NotFoundException("ProductVariant", data.variant_id)

    movement = InventoryMovement(**data.model_dump())
    db.add(movement)

    # Update stock
    variant.stock_quantity += data.quantity
    if variant.stock_quantity < 0:
        variant.stock_quantity = 0

    await db.flush()
    return movement


from src.modules.products.models import ProductVariant  # noqa: E402, F401
