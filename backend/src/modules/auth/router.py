"""
Auth Module — API Router
===========================
Authentication and user management endpoints.
"""

from fastapi import APIRouter, Depends

from src.core.dependencies import CurrentUser, DbSession, Pagination, require_role
from src.core.pagination import PaginatedResponse
from src.modules.auth.repository import AuthRepository
from src.modules.auth.schemas import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
)
from src.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_service(db: DbSession) -> AuthService:
    return AuthService(AuthRepository(db))


# ── Authentication Endpoints ────────────────────────────────────────────────


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: RegisterRequest, service: AuthService = Depends(get_service)):
    """Register a new user account."""
    result = await service.register(data)
    return result


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, service: AuthService = Depends(get_service)):
    """Login with email and password."""
    result = await service.login(data.email, data.password)
    return result


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest, service: AuthService = Depends(get_service)
):
    """Refresh access token."""
    result = await service.refresh_token(data.refresh_token)
    return result


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    data: ForgotPasswordRequest, service: AuthService = Depends(get_service)
):
    """Initiate password reset flow."""
    result = await service.forgot_password(data.email)
    return result


# ── Profile Endpoints ───────────────────────────────────────────────────────


@router.get("/me", response_model=UserResponse)
async def get_profile(user: CurrentUser):
    """Get current user profile."""
    return user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    data: UpdateProfileRequest,
    user: CurrentUser,
    service: AuthService = Depends(get_service),
):
    """Update current user profile."""
    return await service.update_profile(user.id, data)


@router.post("/me/change-password", response_model=MessageResponse)
async def change_password(
    data: ChangePasswordRequest,
    user: CurrentUser,
    service: AuthService = Depends(get_service),
):
    """Change password."""
    await service.change_password(user.id, data.current_password, data.new_password)
    return {"message": "Password changed successfully"}


# ── Address Endpoints ───────────────────────────────────────────────────────


@router.get("/me/addresses", response_model=list[AddressResponse])
async def get_addresses(
    user: CurrentUser, service: AuthService = Depends(get_service)
):
    """Get all addresses for current user."""
    return await service.get_addresses(user.id)


@router.post("/me/addresses", response_model=AddressResponse, status_code=201)
async def create_address(
    data: AddressCreate,
    user: CurrentUser,
    service: AuthService = Depends(get_service),
):
    """Create a new address."""
    return await service.create_address(user.id, data)


@router.put("/me/addresses/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    user: CurrentUser,
    service: AuthService = Depends(get_service),
):
    """Update an address."""
    return await service.update_address(user.id, address_id, data)


@router.delete("/me/addresses/{address_id}", status_code=204)
async def delete_address(
    address_id: int,
    user: CurrentUser,
    service: AuthService = Depends(get_service),
):
    """Delete an address."""
    await service.delete_address(user.id, address_id)


# ── Admin: User Management ──────────────────────────────────────────────────


@router.get(
    "/users",
    response_model=PaginatedResponse[UserResponse],
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)
async def list_users(
    pagination: Pagination,
    search: str | None = None,
    segment: str | None = None,
    service: AuthService = Depends(get_service),
):
    """List all users (admin only)."""
    repo = service.repo
    users, total = await repo.get_all_users(
        offset=pagination.offset,
        limit=pagination.page_size,
        search=search,
        segment=segment,
    )
    return PaginatedResponse.create(users, total, pagination.page, pagination.page_size)
