"""
Orders Module — Repository
=============================
Database access for orders.
"""

import random
import string
from datetime import UTC, datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.orders.models import Order, OrderItem, OrderTimeline


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items),
                selectinload(Order.timeline),
            )
            .where(Order.id == order_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_order_number(self, order_number: str) -> Order | None:
        stmt = (
            select(Order)
            .options(selectinload(Order.items), selectinload(Order.timeline))
            .where(Order.order_number == order_number)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_orders(
        self, user_id: int, offset: int = 0, limit: int = 20
    ) -> tuple[list[Order], int]:
        count_stmt = select(func.count(Order.id)).where(Order.user_id == user_id)
        total = (await self.db.execute(count_stmt)).scalar() or 0

        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def get_all_orders(
        self,
        offset: int = 0,
        limit: int = 20,
        status: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Order], int]:
        conditions = []
        if status:
            conditions.append(Order.status == status)
        if search:
            conditions.append(Order.order_number.ilike(f"%{search}%"))

        count_stmt = select(func.count(Order.id))
        stmt = select(Order).options(selectinload(Order.items))

        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
            stmt = stmt.where(and_(*conditions))

        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(Order.created_at.desc()).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def create(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        return await self.get_by_id(order.id)  # type: ignore

    async def update(self, order: Order) -> Order:
        await self.db.flush()
        return order

    async def add_timeline_event(
        self, order_id: int, status: str, title: str,
        description: str | None = None, created_by: str | None = None
    ) -> OrderTimeline:
        event = OrderTimeline(
            order_id=order_id,
            status=status,
            title=title,
            description=description,
            created_by=created_by,
        )
        self.db.add(event)
        await self.db.flush()
        return event

    @staticmethod
    def generate_order_number() -> str:
        timestamp = datetime.now(UTC).strftime("%y%m%d")
        random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"PDB-{timestamp}-{random_part}"

    # ── Analytics Queries ────────────────────────────────────────────────

    async def count_orders(self, status: str | None = None) -> int:
        stmt = select(func.count(Order.id))
        if status:
            stmt = stmt.where(Order.status == status)
        return (await self.db.execute(stmt)).scalar() or 0

    async def total_revenue(self) -> float:
        stmt = select(func.sum(Order.total)).where(
            Order.status.in_(["confirmed", "processing", "shipped", "delivered"])
        )
        return float((await self.db.execute(stmt)).scalar() or 0)

    async def revenue_by_period(self, days: int = 30) -> list[dict]:
        from datetime import timedelta
        start_date = datetime.now(UTC) - timedelta(days=days)
        stmt = (
            select(
                func.date(Order.created_at).label("date"),
                func.sum(Order.total).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .where(
                Order.created_at >= start_date,
                Order.status.in_(["confirmed", "processing", "shipped", "delivered"]),
            )
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
        )
        result = await self.db.execute(stmt)
        return [
            {"date": str(row.date), "revenue": float(row.revenue), "orders": row.orders}
            for row in result.all()
        ]
