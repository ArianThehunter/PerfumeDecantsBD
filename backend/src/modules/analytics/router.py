"""
Analytics Module — API Router
==============================
Business intelligence, sales analytics, and dashboard metrics.
"""

from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import selectinload

from src.core.dependencies import DbSession as DbSessionDep, require_role
from src.modules.orders.models import Order, OrderItem
from src.modules.products.models import Product, ProductVariant, Brand, Category, product_categories
from src.modules.auth.models import User

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)

# ── Schemas ──────────────────────────────────────────────────────────────────

class KPIMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    average_order_value: float
    total_profit: float
    revenue_growth_pct: float
    order_growth_pct: float

class RevenueChartItem(BaseModel):
    date: str
    revenue: float
    orders: int
    profit: float

class CategoryShareItem(BaseModel):
    category_name: str
    revenue: float
    sales_count: int

class BrandShareItem(BaseModel):
    brand_name: str
    revenue: float
    sales_count: int

class ProductPerformanceItem(BaseModel):
    product_id: int
    product_name: str
    brand_name: str
    sku_count: int
    total_sold: int
    revenue: float
    avg_rating: float

class CustomerSegmentItem(BaseModel):
    segment: str
    count: int
    revenue: float
    avg_clv: float

class InventoryValuation(BaseModel):
    total_stock: int
    total_cost_value: float
    total_retail_value: float
    potential_profit: float

# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=KPIMetrics)
async def get_dashboard_kpis(db: DbSessionDep):
    """Get high-level business KPI metrics for the store owner dashboard."""
    # Current period (last 30 days) vs previous period (30-60 days ago)
    now = datetime.now(UTC)
    last_30_days = now - timedelta(days=30)
    last_60_days = now - timedelta(days=60)

    # 1. Total Revenue (Delivered/Shipped/Confirmed/Paid orders)
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    # Current 30 days revenue
    current_rev_stmt = select(func.sum(Order.total)).where(
        and_(Order.created_at >= last_30_days, Order.status.in_(active_statuses))
    )
    current_rev = float((await db.execute(current_rev_stmt)).scalar() or 0.0)

    # Previous 30 days revenue
    prev_rev_stmt = select(func.sum(Order.total)).where(
        and_(
            Order.created_at >= last_60_days,
            Order.created_at < last_30_days,
            Order.status.in_(active_statuses)
        )
    )
    prev_rev = float((await db.execute(prev_rev_stmt)).scalar() or 0.0)

    # Current 30 days orders
    current_orders_stmt = select(func.count(Order.id)).where(
        and_(Order.created_at >= last_30_days, Order.status.in_(active_statuses))
    )
    current_orders = int((await db.execute(current_orders_stmt)).scalar() or 0)

    # Previous 30 days orders
    prev_orders_stmt = select(func.count(Order.id)).where(
        and_(
            Order.created_at >= last_60_days,
            Order.created_at < last_30_days,
            Order.status.in_(active_statuses)
        )
    )
    prev_orders = int((await db.execute(prev_orders_stmt)).scalar() or 0)

    # Total unique customers who ordered
    cust_stmt = select(func.count(func.distinct(Order.user_id))).where(
        Order.status.in_(active_statuses)
    )
    total_customers = int((await db.execute(cust_stmt)).scalar() or 0)

    # Average Order Value (AOV)
    aov = current_rev / current_orders if current_orders > 0 else 0.0

    # Total cost of current items sold (to calculate profit)
    cost_stmt = (
        select(func.sum(OrderItem.quantity * func.coalesce(ProductVariant.cost_price, ProductVariant.price * 0.6)))
        .join(ProductVariant, OrderItem.variant_id == ProductVariant.id, isouter=True)
        .join(Order, OrderItem.order_id == Order.id)
        .where(and_(Order.created_at >= last_30_days, Order.status.in_(active_statuses)))
    )
    total_cost = float((await db.execute(cost_stmt)).scalar() or 0.0)
    profit = current_rev - total_cost

    # Growth rates
    revenue_growth = ((current_rev - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0
    order_growth = ((current_orders - prev_orders) / prev_orders * 100.0) if prev_orders > 0 else 0.0

    return KPIMetrics(
        total_revenue=current_rev,
        total_orders=current_orders,
        total_customers=total_customers,
        average_order_value=aov,
        total_profit=profit,
        revenue_growth_pct=round(revenue_growth, 2),
        order_growth_pct=round(order_growth, 2),
    )

@router.get("/revenue", response_model=list[RevenueChartItem])
async def get_revenue_analytics(
    db: DbSessionDep,
    start_date: str | None = Query(None, description="ISO date YYYY-MM-DD"),
    end_date: str | None = Query(None, description="ISO date YYYY-MM-DD"),
):
    """Get time-series revenue, orders, and profit analysis."""
    # Date bounds
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.now(UTC) - timedelta(days=30)
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    else:
        end = datetime.now(UTC)

    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    # Query orders and group by day
    # We aggregate total, count, and estimated cost (profit)
    # Using SQL date function for compatibility
    stmt = (
        select(
            func.date(Order.created_at).label("day"),
            func.sum(Order.total).label("revenue"),
            func.count(Order.id).label("orders"),
            # Cost calculation
            func.sum(
                OrderItem.quantity * func.coalesce(ProductVariant.cost_price, ProductVariant.price * 0.6)
            ).label("cost")
        )
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(ProductVariant, OrderItem.variant_id == ProductVariant.id, isouter=True)
        .where(
            and_(
                Order.created_at >= start,
                Order.created_at < end,
                Order.status.in_(active_statuses)
            )
        )
        .group_by(func.date(Order.created_at))
        .order_by("day")
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    chart_data = []
    for row in rows:
        rev = float(row.revenue or 0.0)
        cost = float(row.cost or 0.0)
        chart_data.append(RevenueChartItem(
            date=str(row.day),
            revenue=rev,
            orders=int(row.orders or 0),
            profit=rev - cost,
        ))
        
    return chart_data

@router.get("/categories", response_model=list[CategoryShareItem])
async def get_category_analytics(db: DbSessionDep):
    """Get revenue share distribution by categories."""
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    stmt = (
        select(
            Category.name.label("category_name"),
            func.sum(OrderItem.total_price).label("revenue"),
            func.sum(OrderItem.quantity).label("sales_count")
        )
        .join(OrderItem, OrderItem.variant_id == ProductVariant.id)
        .join(Product, ProductVariant.product_id == Product.id)
        .join(product_categories, product_categories.c.product_id == Product.id)
        .join(Category, product_categories.c.category_id == Category.id)
        .join(Order, OrderItem.order_id == Order.id)
        .where(Order.status.in_(active_statuses))
        .group_by(Category.name)
        .order_by(desc("revenue"))
        .limit(10)
    )
    
    result = await db.execute(stmt)
    return [
        CategoryShareItem(
            category_name=row.category_name,
            revenue=float(row.revenue or 0.0),
            sales_count=int(row.sales_count or 0)
        )
        for row in result.all()
    ]

@router.get("/brands", response_model=list[BrandShareItem])
async def get_brand_analytics(db: DbSessionDep):
    """Get revenue share distribution by perfume houses (brands)."""
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    stmt = (
        select(
            Brand.name.label("brand_name"),
            func.sum(OrderItem.total_price).label("revenue"),
            func.sum(OrderItem.quantity).label("sales_count")
        )
        .join(OrderItem, OrderItem.variant_id == ProductVariant.id)
        .join(Product, ProductVariant.product_id == Product.id)
        .join(Brand, Product.brand_id == Brand.id)
        .join(Order, OrderItem.order_id == Order.id)
        .where(Order.status.in_(active_statuses))
        .group_by(Brand.name)
        .order_by(desc("revenue"))
        .limit(15)
    )
    
    result = await db.execute(stmt)
    return [
        BrandShareItem(
            brand_name=row.brand_name,
            revenue=float(row.revenue or 0.0),
            sales_count=int(row.sales_count or 0)
        )
        for row in result.all()
    ]

@router.get("/products", response_model=list[ProductPerformanceItem])
async def get_product_performance(
    db: DbSessionDep,
    limit: int = Query(10, ge=1, le=100)
):
    """Get best-selling and top-performing products catalog table metrics."""
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    stmt = (
        select(
            Product.id,
            Product.name,
            Brand.name.label("brand_name"),
            func.count(func.distinct(ProductVariant.id)).label("sku_count"),
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.total_price).label("revenue"),
            Product.avg_rating
        )
        .join(ProductVariant, ProductVariant.product_id == Product.id)
        .join(Brand, Product.brand_id == Brand.id)
        .join(OrderItem, OrderItem.variant_id == ProductVariant.id, isouter=True)
        .join(Order, OrderItem.order_id == Order.id, isouter=True)
        # Filters to make sure orders are paid/valid
        .where(and_(
            func.coalesce(Order.status, "confirmed").in_(active_statuses)
        ))
        .group_by(Product.id, Product.name, Brand.name, Product.avg_rating)
        .order_by(desc("total_sold"))
        .limit(limit)
    )
    
    result = await db.execute(stmt)
    return [
        ProductPerformanceItem(
            product_id=row.id,
            product_name=row.name,
            brand_name=row.brand_name,
            sku_count=int(row.sku_count or 0),
            total_sold=int(row.total_sold or 0),
            revenue=float(row.revenue or 0.0),
            avg_rating=float(row.avg_rating or 0.0)
        )
        for row in result.all()
    ]

@router.get("/customers", response_model=list[CustomerSegmentItem])
async def get_customer_segments(db: DbSessionDep):
    """Get customer segmentation and lifetime value statistics."""
    # Let's perform a simple grouping/query to divide customers into VIP, Active, At-Risk, Churned
    # based on their lifetime spending and order dates.
    now = datetime.now(UTC)
    active_cut = now - timedelta(days=90)
    at_risk_cut = now - timedelta(days=180)

    # Subquery to compute CLV and Last Purchase Date per user
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]
    
    stmt = (
        select(
            User.id,
            func.sum(Order.total).label("clv"),
            func.max(Order.created_at).label("last_purchase")
        )
        .join(Order, Order.user_id == User.id)
        .where(Order.status.in_(active_statuses))
        .group_by(User.id)
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    # Classify in memory
    segments = {
        "VIP ($500+ spend)": {"count": 0, "revenue": 0.0, "clv_sum": 0.0},
        "Active (last 90 days)": {"count": 0, "revenue": 0.0, "clv_sum": 0.0},
        "At Risk (90-180 days idle)": {"count": 0, "revenue": 0.0, "clv_sum": 0.0},
        "Churned (180+ days idle)": {"count": 0, "revenue": 0.0, "clv_sum": 0.0},
    }
    
    for row in rows:
        clv = float(row.clv or 0.0)
        last_date = row.last_purchase
        
        if clv >= 500.0:
            key = "VIP ($500+ spend)"
        elif last_date >= active_cut:
            key = "Active (last 90 days)"
        elif last_date >= at_risk_cut:
            key = "At Risk (90-180 days idle)"
        else:
            key = "Churned (180+ days idle)"
            
        segments[key]["count"] += 1
        segments[key]["revenue"] += clv
        segments[key]["clv_sum"] += clv
        
    return [
        CustomerSegmentItem(
            segment=k,
            count=v["count"],
            revenue=v["revenue"],
            avg_clv=v["clv_sum"] / v["count"] if v["count"] > 0 else 0.0
        )
        for k, v in segments.items()
    ]

@router.get("/inventory", response_model=InventoryValuation)
async def get_inventory_valuation(db: DbSessionDep):
    """Get stock inventory asset valuation and potential profit margins."""
    stmt = select(
        func.sum(ProductVariant.stock_quantity).label("total_stock"),
        func.sum(ProductVariant.stock_quantity * func.coalesce(ProductVariant.cost_price, ProductVariant.price * 0.6)).label("total_cost"),
        func.sum(ProductVariant.stock_quantity * ProductVariant.price).label("total_retail")
    ).where(ProductVariant.is_active == True)  # noqa: E712
    
    result = await db.execute(stmt)
    row = result.one()
    
    total_stock = int(row.total_stock or 0)
    total_cost = float(row.total_cost or 0.0)
    total_retail = float(row.total_retail or 0.0)
    
    return InventoryValuation(
        total_stock=total_stock,
        total_cost_value=total_cost,
        total_retail_value=total_retail,
        potential_profit=total_retail - total_cost,
    )
