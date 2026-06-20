"""
Cart Module — Router
======================
Shopping cart and wishlist API endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from src.core.dependencies import CurrentUser, DbSession
from src.core.exceptions import NotFoundException, ValidationException
from src.modules.cart.models import Cart, CartItem, Wishlist, WishlistItem
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/cart", tags=["Cart"])
wishlist_router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


# ── Schemas ──────────────────────────────────────────────────────────────────


class CartItemAdd(BaseModel):
    variant_id: int
    quantity: int = Field(ge=1, default=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=0)


class CartItemResponse(BaseModel):
    id: int
    variant_id: int
    quantity: int
    saved_for_later: bool = False
    variant_name: str | None = None
    product_name: str | None = None
    price: float | None = None
    image_url: str | None = None

    model_config = {"from_attributes": True}


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse] = []
    total: float = 0.0

    model_config = {"from_attributes": True}


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    added_at: datetime

    model_config = {"from_attributes": True}


# ── Cart Endpoints ───────────────────────────────────────────────────────────


@router.get("", response_model=CartResponse)
async def get_cart(user: CurrentUser, db: DbSession):
    """Get current user's cart."""
    stmt = (
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.variant))
        .where(Cart.user_id == user.id)
    )
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        await db.flush()

    items_response = []
    total = 0.0
    for item in cart.items:
        if not item.saved_for_later:
            price = float(item.variant.discount_price or item.variant.price) if item.variant else 0
            total += price * item.quantity
        items_response.append(CartItemResponse(
            id=item.id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            saved_for_later=item.saved_for_later,
        ))

    return CartResponse(id=cart.id, items=items_response, total=total)


@router.post("/items", status_code=201)
async def add_to_cart(data: CartItemAdd, user: CurrentUser, db: DbSession):
    """Add item to cart."""
    # Get or create cart
    stmt = select(Cart).where(Cart.user_id == user.id)
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        await db.flush()

    # Check if item already exists
    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.variant_id == data.variant_id
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        existing.quantity += data.quantity
    else:
        item = CartItem(cart_id=cart.id, variant_id=data.variant_id, quantity=data.quantity)
        db.add(item)

    await db.flush()
    return {"message": "Item added to cart"}


@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, data: CartItemUpdate, user: CurrentUser, db: DbSession):
    """Update cart item quantity."""
    item = await db.get(CartItem, item_id)
    if not item:
        raise NotFoundException("Cart item", item_id)

    if data.quantity == 0:
        await db.delete(item)
    else:
        item.quantity = data.quantity

    await db.flush()
    return {"message": "Cart updated"}


@router.delete("/items/{item_id}", status_code=204)
async def remove_from_cart(item_id: int, user: CurrentUser, db: DbSession):
    """Remove item from cart."""
    item = await db.get(CartItem, item_id)
    if item:
        await db.delete(item)
        await db.flush()


@router.delete("", status_code=204)
async def clear_cart(user: CurrentUser, db: DbSession):
    """Clear all items from cart."""
    stmt = select(Cart).where(Cart.user_id == user.id)
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()
    if cart:
        await db.execute(delete(CartItem).where(CartItem.cart_id == cart.id))
        await db.flush()


# ── Wishlist Endpoints ───────────────────────────────────────────────────────


@wishlist_router.get("", response_model=list[WishlistItemResponse])
async def get_wishlist(user: CurrentUser, db: DbSession):
    """Get current user's wishlist."""
    stmt = select(Wishlist).options(selectinload(Wishlist.items)).where(Wishlist.user_id == user.id)
    result = await db.execute(stmt)
    wishlist = result.scalar_one_or_none()
    if not wishlist:
        return []
    return wishlist.items


@wishlist_router.post("/items/{product_id}", status_code=201)
async def add_to_wishlist(product_id: int, user: CurrentUser, db: DbSession):
    """Add product to wishlist."""
    stmt = select(Wishlist).where(Wishlist.user_id == user.id)
    result = await db.execute(stmt)
    wishlist = result.scalar_one_or_none()
    if not wishlist:
        wishlist = Wishlist(user_id=user.id)
        db.add(wishlist)
        await db.flush()

    # Check if already exists
    stmt = select(WishlistItem).where(
        WishlistItem.wishlist_id == wishlist.id, WishlistItem.product_id == product_id
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        return {"message": "Already in wishlist"}

    item = WishlistItem(wishlist_id=wishlist.id, product_id=product_id)
    db.add(item)
    await db.flush()
    return {"message": "Added to wishlist"}


@wishlist_router.delete("/items/{product_id}", status_code=204)
async def remove_from_wishlist(product_id: int, user: CurrentUser, db: DbSession):
    """Remove product from wishlist."""
    stmt = select(Wishlist).where(Wishlist.user_id == user.id)
    result = await db.execute(stmt)
    wishlist = result.scalar_one_or_none()
    if wishlist:
        await db.execute(
            delete(WishlistItem).where(
                WishlistItem.wishlist_id == wishlist.id,
                WishlistItem.product_id == product_id,
            )
        )
        await db.flush()
