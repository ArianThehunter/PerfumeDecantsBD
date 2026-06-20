"""
PerfumeDecantBD — Exception Handlers
======================================
Custom exception classes and FastAPI exception handlers.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger()


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=404,
        )


class DuplicateException(AppException):
    """Duplicate resource."""

    def __init__(self, resource: str, field: str):
        super().__init__(
            message=f"{resource} with this {field} already exists",
            status_code=409,
        )


class ForbiddenException(AppException):
    """Access forbidden."""

    def __init__(self, message: str = "Access denied"):
        super().__init__(message=message, status_code=403)


class ValidationException(AppException):
    """Validation error."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message=message, status_code=422, details=details)


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers with the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning(
            "Application error",
            error=exc.message,
            status_code=exc.status_code,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unhandled exception",
            error=str(exc),
            path=str(request.url),
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
        )
