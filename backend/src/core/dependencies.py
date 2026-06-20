"""
PerfumeDecantBD — Shared Dependencies
=======================================
FastAPI dependency injection for auth, pagination, and permissions.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.security import decode_token

# Security scheme
security = HTTPBearer(auto_error=False)

# Type aliases
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: DbSession,
) -> dict:
    """Extract and validate the current user from JWT token."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # Import here to avoid circular imports
    from src.modules.auth.repository import AuthRepository

    repo = AuthRepository(db)
    user = await repo.get_by_id(int(payload["sub"]))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    return user


async def get_optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: DbSession,
):
    """Get current user if authenticated, None otherwise."""
    if not credentials:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


CurrentUser = Annotated[dict, Depends(get_current_user)]
OptionalUser = Annotated[dict | None, Depends(get_optional_user)]


def require_role(*roles: str):
    """Dependency factory that checks user role."""

    async def role_checker(user: CurrentUser):
        # Import here to avoid circular imports
        from src.modules.auth.repository import AuthRepository

        user_roles = [r.name for r in user.roles] if hasattr(user, "roles") else []
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {', '.join(roles)}",
            )
        return user

    return role_checker


class PaginationParams:
    """Common pagination parameters."""

    def __init__(
        self,
        page: Annotated[int, Query(ge=1, description="Page number")] = 1,
        page_size: Annotated[
            int, Query(ge=1, le=100, alias="pageSize", description="Items per page")
        ] = 20,
    ):
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size


Pagination = Annotated[PaginationParams, Depends()]
