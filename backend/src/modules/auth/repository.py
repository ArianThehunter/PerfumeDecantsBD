"""
Auth Module — Repository
==========================
Database access layer for users and auth operations.
"""

from datetime import UTC, datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.modules.auth.models import User, Role, Address, user_roles


class AuthRepository:
    """Repository for user-related database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID with roles eagerly loaded."""
        stmt = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email with roles eagerly loaded."""
        stmt = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.flush()
        # Reload with relationships
        return await self.get_by_id(user.id)  # type: ignore

    async def update(self, user: User) -> User:
        """Update an existing user."""
        await self.db.flush()
        return user

    async def get_role_by_name(self, name: str) -> Role | None:
        """Get role by name."""
        stmt = select(Role).where(Role.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def assign_role(self, user_id: int, role_id: int) -> None:
        """Assign a role to a user."""
        from sqlalchemy import insert
        stmt = insert(user_roles).values(user_id=user_id, role_id=role_id)
        await self.db.execute(stmt)

    async def get_all_users(
        self,
        offset: int = 0,
        limit: int = 20,
        search: str | None = None,
        segment: str | None = None,
    ) -> tuple[list[User], int]:
        """Get paginated users with optional filters."""
        stmt = select(User).options(selectinload(User.roles))
        count_stmt = select(func.count(User.id))

        if search:
            search_filter = f"%{search}%"
            filter_cond = (
                User.email.ilike(search_filter)
                | User.first_name.ilike(search_filter)
                | User.last_name.ilike(search_filter)
            )
            stmt = stmt.where(filter_cond)
            count_stmt = count_stmt.where(filter_cond)

        if segment:
            stmt = stmt.where(User.segment == segment)
            count_stmt = count_stmt.where(User.segment == segment)

        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.order_by(User.created_at.desc()).offset(offset).limit(limit)
        result = await self.db.execute(stmt)

        return list(result.scalars().all()), total

    async def update_last_login(self, user: User) -> None:
        """Update the last login timestamp."""
        user.last_login_at = datetime.now(UTC)
        await self.db.flush()

    # ── Address Operations ───────────────────────────────────────────────

    async def get_addresses(self, user_id: int) -> list[Address]:
        """Get all addresses for a user."""
        stmt = select(Address).where(Address.user_id == user_id).order_by(Address.is_default.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_address(self, address_id: int, user_id: int) -> Address | None:
        """Get a specific address."""
        stmt = select(Address).where(Address.id == address_id, Address.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_address(self, address: Address) -> Address:
        """Create a new address."""
        if address.is_default:
            await self._unset_default_address(address.user_id)
        self.db.add(address)
        await self.db.flush()
        return address

    async def update_address(self, address: Address) -> Address:
        """Update an address."""
        if address.is_default:
            await self._unset_default_address(address.user_id)
        await self.db.flush()
        return address

    async def delete_address(self, address: Address) -> None:
        """Delete an address."""
        await self.db.delete(address)
        await self.db.flush()

    async def _unset_default_address(self, user_id: int) -> None:
        """Unset all default addresses for a user."""
        from sqlalchemy import update
        stmt = (
            update(Address)
            .where(Address.user_id == user_id, Address.is_default == True)  # noqa: E712
            .values(is_default=False)
        )
        await self.db.execute(stmt)

    # ── Statistics ───────────────────────────────────────────────────────

    async def count_users(self) -> int:
        """Count total users."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar() or 0

    async def count_users_by_segment(self) -> dict[str, int]:
        """Count users grouped by segment."""
        stmt = (
            select(User.segment, func.count(User.id))
            .group_by(User.segment)
        )
        result = await self.db.execute(stmt)
        return {row[0] or "Unclassified": row[1] for row in result.all()}
