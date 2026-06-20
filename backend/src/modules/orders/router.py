"""
Orders Module — Service & Router
====================================
"""

from fastapi import APIRouter, Depends

from src.core.dependencies import CurrentUser, DbSession, Pagination, require_role
from src.core.exceptions import NotFoundException, ValidationException
from src.core.pagination import PaginatedResponse
from src.modules.orders.models import Order, OrderItem
from src.modules.orders.repository import OrderRepository
from src.modules.orders.schemas import (
    OrderCreate, OrderResponse, OrderListResponse, OrderStatusUpdate,
)
from src.modules.products.models import ProductVariant
from sqlalchemy import select

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_repo(db: DbSession) -> OrderRepository:
    return OrderRepository(db)


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    data: OrderCreate,
    user: CurrentUser,
    db: DbSession,
    repo: OrderRepository = Depends(get_repo),
):
    """Create a new order from cart items."""
    order_items = []
    subtotal = 0.0

    for item_data in data.items:
        variant = await db.get(ProductVariant, item_data.variant_id)
        if not variant:
            raise ValidationException(f"Variant {item_data.variant_id} not found")
        if variant.stock_quantity < item_data.quantity:
            raise ValidationException(f"Insufficient stock for {variant.name}")

        unit_price = float(variant.discount_price or variant.price)
        total_price = unit_price * item_data.quantity
        subtotal += total_price

        # Get product info
        from src.modules.products.models import Product
        product = await db.get(Product, variant.product_id)

        order_items.append(
            OrderItem(
                variant_id=variant.id,
                product_name=product.name if product else "Unknown",
                variant_name=variant.name,
                sku=variant.sku,
                quantity=item_data.quantity,
                unit_price=unit_price,
                total_price=total_price,
            )
        )

        # Decrease stock
        variant.stock_quantity -= item_data.quantity

    # Calculate totals
    tax_rate = 0.05  # 5% tax
    tax_amount = subtotal * tax_rate
    shipping_cost = 0 if subtotal > 5000 else 150  # Free shipping over 5000
    total = subtotal + tax_amount + shipping_cost

    order = Order(
        order_number=OrderRepository.generate_order_number(),
        user_id=user.id,
        status="pending",
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax_amount=tax_amount,
        total=total,
        shipping_address=data.shipping_address,
        billing_address=data.billing_address,
        shipping_method=data.shipping_method,
        payment_method=data.payment_method,
        coupon_code=data.coupon_code,
        customer_note=data.customer_note,
        items=order_items,
    )

    order = await repo.create(order)

    # Add timeline event
    await repo.add_timeline_event(
        order.id, "pending", "Order placed", f"Order {order.order_number} was placed"
    )

    # Update user stats
    user.total_orders += 1
    user.lifetime_value += total

    return await repo.get_by_id(order.id)


@router.get("/my-orders", response_model=PaginatedResponse[OrderListResponse])
async def get_my_orders(
    pagination: Pagination,
    user: CurrentUser,
    repo: OrderRepository = Depends(get_repo),
):
    """Get current user's orders."""
    orders, total = await repo.get_user_orders(user.id, pagination.offset, pagination.page_size)
    return PaginatedResponse.create(orders, total, pagination.page, pagination.page_size)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user: CurrentUser,
    repo: OrderRepository = Depends(get_repo),
):
    """Get order details."""
    order = await repo.get_by_id(order_id)
    if not order:
        raise NotFoundException("Order", order_id)

    # Check ownership (admins can see all)
    admin_roles = {"SuperAdmin", "Manager", "SalesStaff"}
    user_roles = set(user.role_names) if hasattr(user, "role_names") else set()
    if order.user_id != user.id and not user_roles.intersection(admin_roles):
        raise NotFoundException("Order", order_id)

    return order


@router.put(
    "/{order_id}/status",
    response_model=OrderResponse,
    dependencies=[Depends(require_role("SuperAdmin", "Manager", "SalesStaff"))],
)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    user: CurrentUser,
    repo: OrderRepository = Depends(get_repo),
):
    """Update order status (admin)."""
    order = await repo.get_by_id(order_id)
    if not order:
        raise NotFoundException("Order", order_id)

    old_status = order.status
    order.status = data.status

    # Set timestamps
    from datetime import UTC, datetime
    if data.status == "shipped":
        order.shipped_at = datetime.now(UTC)
    elif data.status == "delivered":
        order.delivered_at = datetime.now(UTC)

    await repo.update(order)
    await repo.add_timeline_event(
        order.id,
        data.status,
        f"Status changed to {data.status}",
        data.note or f"Changed from {old_status} to {data.status}",
        created_by=user.full_name if hasattr(user, "full_name") else "Admin",
    )

    return await repo.get_by_id(order_id)


@router.get(
    "",
    response_model=PaginatedResponse[OrderListResponse],
    dependencies=[Depends(require_role("SuperAdmin", "Manager", "SalesStaff"))],
)
async def list_all_orders(
    pagination: Pagination,
    status: str | None = None,
    search: str | None = None,
    repo: OrderRepository = Depends(get_repo),
):
    """List all orders (admin)."""
    orders, total = await repo.get_all_orders(
        pagination.offset, pagination.page_size, status, search
    )
    return PaginatedResponse.create(orders, total, pagination.page, pagination.page_size)
