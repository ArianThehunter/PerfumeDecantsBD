"""
AI Insights Module — API Router
=================================
Automated business observations, forecasts, and actionable recommendations.
"""

from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func, and_, desc

from src.core.dependencies import DbSession, DbSession as DbSessionDep, require_role
from src.modules.orders.models import Order, OrderItem
from src.modules.products.models import Product, ProductVariant, Brand

router = APIRouter(
    prefix="/insights",
    tags=["AI Insights"],
    dependencies=[Depends(require_role("SuperAdmin", "Manager"))],
)

# ── Schemas ──────────────────────────────────────────────────────────────────

class InsightCard(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # info, warning, success, opportunity
    category: str  # inventory, revenue, customers, product
    impact_score: int  # 1-10 scale
    action_label: str | None = None
    action_link: str | None = None

# ── Router Endpoints ─────────────────────────────────────────────────────────

@router.get("", response_model=list[InsightCard])
async def get_ai_insights(db: DbSessionDep):
    """Retrieve auto-generated, rule-based business insights and recommendations."""
    insights = []
    
    # ── 1. Restock Recommendations (Inventory) ──────────────────────────────
    # Identify items below safety stock or out of stock
    stmt = (
        select(
            Product.name.label("product_name"),
            ProductVariant.name.label("variant_name"),
            ProductVariant.stock_quantity,
            ProductVariant.safety_stock,
            ProductVariant.price
        )
        .join(Product, ProductVariant.product_id == Product.id)
        .where(
            and_(
                ProductVariant.stock_quantity <= ProductVariant.safety_stock,
                ProductVariant.is_active == True  # noqa: E712
            )
        )
        .limit(5)
    )
    low_stock_rows = (await db.execute(stmt)).all()
    
    if low_stock_rows:
        items_list = ", ".join([f"{r.product_name} ({r.variant_name})" for r in low_stock_rows[:3]])
        if len(low_stock_rows) > 3:
            items_list += f", and {len(low_stock_rows) - 3} others"
            
        insights.append(InsightCard(
            id="inv_restock_alert",
            title="Restock Warning: High-Demand SKUs Running Low",
            description=f"The following products are at or below their safety stock thresholds: {items_list}. Consider raising purchase orders to prevent stockouts.",
            severity="warning",
            category="inventory",
            impact_score=8,
            action_label="Manage Inventory",
            action_link="/admin/inventory"
        ))

    # ── 2. Revenue Trend Analysis (Revenue) ──────────────────────────────────
    # Check week-over-week growth
    now = datetime.now(UTC)
    this_week_start = now - timedelta(days=7)
    last_week_start = now - timedelta(days=14)
    active_statuses = ["confirmed", "processing", "shipped", "delivered"]

    rev_this_week = float((await db.execute(
        select(func.sum(Order.total)).where(
            and_(Order.created_at >= this_week_start, Order.status.in_(active_statuses))
        )
    )).scalar() or 0.0)

    rev_last_week = float((await db.execute(
        select(func.sum(Order.total)).where(
            and_(
                Order.created_at >= last_week_start,
                Order.created_at < this_week_start,
                Order.status.in_(active_statuses)
            )
        )
    )).scalar() or 0.0)

    if rev_last_week > 0:
        growth = ((rev_this_week - rev_last_week) / rev_last_week) * 100
        if growth > 5.0:
            insights.append(InsightCard(
                id="rev_upward_trend",
                title=f"Sales Trending Upwards (+{growth:.1f}% WoW)",
                description=f"Weekly revenue reached ${rev_this_week:,.2f}, up from ${rev_last_week:,.2f} last week. Driven by strong weekend sales performance.",
                severity="success",
                category="revenue",
                impact_score=7,
                action_label="View Analytics",
                action_link="/admin/analytics"
            ))
        elif growth < -5.0:
            insights.append(InsightCard(
                id="rev_downward_trend",
                title=f"Weekly Revenue Drop Detected ({growth:.1f}% WoW)",
                description=f"Weekly sales fell to ${rev_this_week:,.2f} compared to ${rev_last_week:,.2f} the previous week. Check if traffic or discount campaigns dropped.",
                severity="warning",
                category="revenue",
                impact_score=7,
                action_label="Run Report",
                action_link="/admin/reports"
            ))
    else:
        # Default starting insight
        insights.append(InsightCard(
            id="rev_baseline",
            title="Analyzing Baseline Revenue Trajectory",
            description="Collecting baseline transaction patterns. Regular week-over-week performance reports will be available soon.",
            severity="info",
            category="revenue",
            impact_score=4,
            action_label="View Sales",
            action_link="/admin/orders"
        ))

    # ── 3. Pareto 80/20 Rule Analysis (Product) ──────────────────────────────
    # See if top products drive the majority of sales
    total_rev = float((await db.execute(
        select(func.sum(OrderItem.total_price))
        .join(Order, OrderItem.order_id == Order.id)
        .where(Order.status.in_(active_statuses))
    )).scalar() or 0.0)

    if total_rev > 0:
        # Get sales per product
        stmt = (
            select(Product.name, func.sum(OrderItem.total_price).label("prod_rev"))
            .join(ProductVariant, ProductVariant.product_id == Product.id)
            .join(OrderItem, OrderItem.variant_id == ProductVariant.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(Order.status.in_(active_statuses))
            .group_by(Product.name)
            .order_by(desc("prod_rev"))
        )
        prod_sales = (await db.execute(stmt)).all()
        
        # Calculate how many products make up 80% of revenue
        running_sum = 0
        top_count = 0
        for row in prod_sales:
            running_sum += float(row.prod_rev or 0.0)
            top_count += 1
            if running_sum >= total_rev * 0.8:
                break
                
        total_products = len(prod_sales)
        if total_products > 0:
            pct_products = (top_count / total_products) * 100
            if pct_products <= 30.0:  # Strong Pareto distribution
                top_names = ", ".join([r.name for r in prod_sales[:2]])
                insights.append(InsightCard(
                    id="product_pareto_concentration",
                    title="Revenue Concentration: 80/20 Rule Active",
                    description=f"Just {pct_products:.1f}% of your catalog ({top_count} products) accounts for 80% of total sales. Your primary drivers are: {top_names}.",
                    severity="opportunity",
                    category="product",
                    impact_score=9,
                    action_label="Focus Catalog",
                    action_link="/admin/products"
                ))

    # ── 4. Slow-Moving Stock (Inventory) ────────────────────────────
    # Find active products with stock > 30 and 0 units sold in the last 30 days
    last_month = now - timedelta(days=30)
    
    # Subquery for items sold in the last 30 days
    sold_subq = (
        select(OrderItem.variant_id)
        .join(Order, OrderItem.order_id == Order.id)
        .where(and_(Order.created_at >= last_month, Order.status.in_(active_statuses)))
        .scalar_subquery()
    )
    
    slow_stmt = (
        select(Product.name, ProductVariant.name.label("vname"), ProductVariant.stock_quantity)
        .join(Product, ProductVariant.product_id == Product.id)
        .where(
            and_(
                ProductVariant.stock_quantity >= 30,
                ProductVariant.is_active == True,  # noqa: E712
                ProductVariant.id.notin_(sold_subq)
            )
        )
        .limit(2)
    )
    slow_rows = (await db.execute(slow_stmt)).all()
    
    if slow_rows:
        slow_list = ", ".join([f"{r.name} ({r.vname})" for r in slow_rows])
        insights.append(InsightCard(
            id="inv_slow_moving",
            title="Dead Stock Warning: Excess Capital Tied Up",
            description=f"Products like {slow_list} have significant stock levels but recorded zero sales in the last 30 days. Consider running a promotional clearance campaign.",
            severity="info",
            category="inventory",
            impact_score=6,
            action_label="Create Discount",
            action_link="/admin/discounts"
        ))

    # ── 5. Average Order Value Uplift opportunity ───────────────────────
    # Look for coupons or bulk sales opportunities
    avg_items_stmt = select(func.avg(OrderItem.quantity)).join(Order, OrderItem.order_id == Order.id).where(Order.status.in_(active_statuses))
    avg_items = float((await db.execute(avg_items_stmt)).scalar() or 0.0)
    
    if 1.0 <= avg_items < 1.8:
        insights.append(InsightCard(
            id="upsell_aov_bundle",
            title="Opportunity: Increase Cart Size via Bundles",
            description=f"Customers purchase an average of only {avg_items:.1f} items per order. Try implementing 'frequently bought together' product recommendations or cross-sell options to boost Average Order Value.",
            severity="opportunity",
            category="customers",
            impact_score=7,
            action_label="Configure Cross-Sells",
            action_link="/admin/settings"
        ))

    return insights
