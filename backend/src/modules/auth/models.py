"""
Auth Module — SQLAlchemy Models
=================================
User, Role, and session management models.
"""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

# Many-to-many: users ↔ roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base):
    """User role for RBAC."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(200))
    permissions: Mapped[str | None] = mapped_column(Text)  # JSON string of permissions
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    users: Mapped[list["User"]] = relationship(secondary=user_roles, back_populates="roles")


class User(Base):
    """Application user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))
    avatar_url: Mapped[str | None] = mapped_column(String(500))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Customer-specific fields
    reward_points: Mapped[int] = mapped_column(Integer, default=0)
    lifetime_value: Mapped[float] = mapped_column(default=0.0)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    segment: Mapped[str | None] = mapped_column(String(50))  # VIP, Active, At-Risk, Churned
    notes: Mapped[str | None] = mapped_column(Text)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, back_populates="users")
    addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all, delete")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    cart: Mapped["Cart | None"] = relationship(back_populates="user", uselist=False)
    wishlist: Mapped["Wishlist | None"] = relationship(back_populates="user", uselist=False)
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def role_names(self) -> list[str]:
        return [r.name for r in self.roles]


class Address(Base):
    """User address for shipping and billing."""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(50), default="Home")  # Home, Office, etc.
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="Bangladesh")
    phone: Mapped[str | None] = mapped_column(String(20))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    user: Mapped["User"] = relationship(back_populates="addresses")


# Forward references for type hints — actual models defined in their respective modules
# These are needed for User relationships
from src.modules.orders.models import Order  # noqa: E402, F401
from src.modules.reviews.models import Review  # noqa: E402, F401
from src.modules.cart.models import Cart, Wishlist  # noqa: E402, F401
from src.modules.notifications.models import Notification  # noqa: E402, F401
