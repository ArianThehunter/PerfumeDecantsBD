"""
PerfumeDecantBD — Middleware
=============================
CORS, rate limiting, request logging, and security middleware.
"""

import time
from collections.abc import Callable

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

# Rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the FastAPI application."""

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"],
    )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        if not request.url.path.startswith("/api/health"):
            logger.info(
                "HTTP request",
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                duration_ms=round(duration_ms, 2),
                client=request.client.host if request.client else "unknown",
            )

        # Add timing header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

        return response

    # Security headers middleware
    @app.middleware("http")
    async def security_headers(request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # Rate limiter state
    app.state.limiter = limiter
