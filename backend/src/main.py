"""
PerfumeDecantBD — Backend Entrypoint
=====================================
FastAPI application core. Registers middleware, exception handlers, database lifecycle, and API routers.
"""

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import structlog

from src.core.config import get_settings
from src.core.database import init_db, close_db
from src.core.middleware import setup_middleware
from src.core.exceptions import register_exception_handlers

# Import routers
from src.modules.auth import auth_router
from src.modules.products import products_router, brands_router, categories_router, collections_router
from src.modules.cart import cart_router, wishlist_router
from src.modules.orders import orders_router
from src.modules.discounts import discounts_router
from src.modules.inventory import inventory_router
from src.modules.notifications import notifications_router
from src.modules.reviews import reviews_router
from src.modules.analytics import analytics_router
from src.modules.ai_insights import insights_router
from src.modules.reports import reports_router

logger = structlog.get_logger()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    logger.info("Starting PerfumeDecantBD API Server", environment=settings.environment)
    if settings.is_development:
        logger.info("Initializing database tables for development")
        await init_db()
    yield
    # Shutdown: Clean up Database connections
    logger.info("Shutting down PerfumeDecantBD API Server")
    await close_db()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Luxury Perfume E-commerce & Business Intelligence Platform API",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# Setup core middleware and handlers
setup_middleware(app)
register_exception_handlers(app)

# Mount Uploads for images / static content
import os
os.makedirs(settings.upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Health check
@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC),
        "version": settings.app_version
    }

# Register API routers under /api prefix
app.include_router(auth_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(brands_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(collections_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(wishlist_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(discounts_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(reviews_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
