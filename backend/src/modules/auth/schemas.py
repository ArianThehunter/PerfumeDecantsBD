"""
Auth Module — Pydantic Schemas
================================
Request/response schemas for authentication endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ──────────────────────────────────────────────────────────


class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(None, max_length=20)


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request."""

    token: str
    new_password: str = Field(min_length=8, max_length=128)


class UpdateProfileRequest(BaseModel):
    """Update user profile request."""

    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)


class ChangePasswordRequest(BaseModel):
    """Change password request."""

    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class AddressCreate(BaseModel):
    """Create address request."""

    label: str = Field(default="Home", max_length=50)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    address_line1: str = Field(max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    city: str = Field(max_length=100)
    state: str | None = Field(None, max_length=100)
    postal_code: str = Field(max_length=20)
    country: str = Field(default="Bangladesh", max_length=100)
    phone: str | None = Field(None, max_length=20)
    is_default: bool = False


class AddressUpdate(BaseModel):
    """Update address request."""

    label: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    phone: str | None = None
    is_default: bool | None = None


# ── Response Schemas ─────────────────────────────────────────────────────────


class RoleResponse(BaseModel):
    """Role in API responses."""

    id: int
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    """User in API responses."""

    id: int
    email: str
    first_name: str
    last_name: str
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    is_verified: bool
    reward_points: int = 0
    segment: str | None = None
    roles: list[RoleResponse] = []
    created_at: datetime
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserBriefResponse(BaseModel):
    """Minimal user info for embedded responses."""

    id: int
    email: str
    first_name: str
    last_name: str
    avatar_url: str | None = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token pair response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class AddressResponse(BaseModel):
    """Address in API responses."""

    id: int
    label: str
    first_name: str
    last_name: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str | None = None
    postal_code: str
    country: str
    phone: str | None = None
    is_default: bool

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str
