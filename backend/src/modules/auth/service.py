"""
Auth Module — Service Layer
==============================
Business logic for authentication and user management.
"""

from src.core.exceptions import DuplicateException, NotFoundException, ValidationException
from src.core.security import (
    create_token_pair,
    decode_token,
    hash_password,
    verify_password,
)
from src.modules.auth.models import User, Address
from src.modules.auth.repository import AuthRepository
from src.modules.auth.schemas import (
    AddressCreate,
    AddressUpdate,
    RegisterRequest,
    UpdateProfileRequest,
)


class AuthService:
    """Service layer for authentication operations."""

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    async def register(self, data: RegisterRequest) -> dict:
        """Register a new user."""
        # Check for existing email
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise DuplicateException("User", "email")

        # Create user
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            segment="Active",
        )
        user = await self.repo.create(user)

        # Assign default customer role
        customer_role = await self.repo.get_role_by_name("Customer")
        if customer_role:
            await self.repo.assign_role(user.id, customer_role.id)
            user = await self.repo.get_by_id(user.id)

        # Generate tokens
        role_name = user.role_names[0] if user.role_names else "Customer"
        tokens = create_token_pair(user.id, user.email, role_name)

        return {**tokens, "user": user}

    async def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValidationException("Invalid email or password")

        if not user.is_active:
            raise ValidationException("Account is deactivated")

        await self.repo.update_last_login(user)

        role_name = user.role_names[0] if user.role_names else "Customer"
        tokens = create_token_pair(user.id, user.email, role_name)

        return {**tokens, "user": user}

    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValidationException("Invalid refresh token")

        user = await self.repo.get_by_id(int(payload["sub"]))
        if not user or not user.is_active:
            raise ValidationException("User not found or inactive")

        role_name = user.role_names[0] if user.role_names else "Customer"
        tokens = create_token_pair(user.id, user.email, role_name)

        return {**tokens, "user": user}

    async def update_profile(self, user_id: int, data: UpdateProfileRequest) -> User:
        """Update user profile."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.phone is not None:
            user.phone = data.phone

        return await self.repo.update(user)

    async def change_password(
        self, user_id: int, current_password: str, new_password: str
    ) -> None:
        """Change user password."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        if not verify_password(current_password, user.password_hash):
            raise ValidationException("Current password is incorrect")

        user.password_hash = hash_password(new_password)
        await self.repo.update(user)

    async def forgot_password(self, email: str) -> dict:
        """Initiate forgot password flow (placeholder)."""
        user = await self.repo.get_by_email(email)
        # Always return success to prevent email enumeration
        return {"message": "If the email exists, a reset link has been sent"}

    # ── Address Operations ───────────────────────────────────────────────

    async def get_addresses(self, user_id: int) -> list[Address]:
        """Get all addresses for a user."""
        return await self.repo.get_addresses(user_id)

    async def create_address(self, user_id: int, data: AddressCreate) -> Address:
        """Create a new address."""
        address = Address(user_id=user_id, **data.model_dump())
        return await self.repo.create_address(address)

    async def update_address(
        self, user_id: int, address_id: int, data: AddressUpdate
    ) -> Address:
        """Update an address."""
        address = await self.repo.get_address(address_id, user_id)
        if not address:
            raise NotFoundException("Address", address_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(address, field, value)

        return await self.repo.update_address(address)

    async def delete_address(self, user_id: int, address_id: int) -> None:
        """Delete an address."""
        address = await self.repo.get_address(address_id, user_id)
        if not address:
            raise NotFoundException("Address", address_id)
        await self.repo.delete_address(address)
