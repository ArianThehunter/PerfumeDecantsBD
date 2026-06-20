"""
Notifications Module — Models & Router
=========================================
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.dependencies import CurrentUser, DbSession, Pagination, require_role
from src.core.pagination import PaginatedResponse


# ── Models ───────────────────────────────────────────────────────────────────


class Notification(Base):
    """User notification."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # order, review, system, promotion, low_stock
    severity: Mapped[str] = mapped_column(String(20), default="info")  # info, warning, success, error
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    link: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    user: Mapped["User"] = relationship(back_populates="notifications")


class AuditLog(Base):
    """System audit trail."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[str | None] = mapped_column(Text)  # JSON
    ip_address: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


# ── Schemas ──────────────────────────────────────────────────────────────────


class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    severity: str
    is_read: bool
    link: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Router ───────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=PaginatedResponse[NotificationResponse])
async def get_notifications(
    pagination: Pagination, user: CurrentUser, db: DbSession
):
    """Get current user's notifications."""
    count_stmt = select(func.count(Notification.id)).where(Notification.user_id == user.id)
    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.page_size)
    )
    result = await db.execute(stmt)
    return PaginatedResponse.create(
        list(result.scalars().all()), total, pagination.page, pagination.page_size
    )


@router.get("/unread-count")
async def get_unread_count(user: CurrentUser, db: DbSession):
    """Get count of unread notifications."""
    count = (
        await db.execute(
            select(func.count(Notification.id)).where(
                Notification.user_id == user.id,
                Notification.is_read == False,  # noqa: E712
            )
        )
    ).scalar() or 0
    return {"count": count}


@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: int, user: CurrentUser, db: DbSession):
    """Mark notification as read."""
    notification = await db.get(Notification, notification_id)
    if notification and notification.user_id == user.id:
        notification.is_read = True
        await db.flush()
    return {"message": "Marked as read"}


@router.put("/read-all")
async def mark_all_as_read(user: CurrentUser, db: DbSession):
    """Mark all notifications as read."""
    from sqlalchemy import update
    await db.execute(
        update(Notification)
        .where(Notification.user_id == user.id, Notification.is_read == False)  # noqa: E712
        .values(is_read=True)
    )
    await db.flush()
    return {"message": "All notifications marked as read"}


from src.modules.auth.models import User  # noqa: E402, F401
