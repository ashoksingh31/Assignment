from fastapi import APIRouter

from app.schemas import StatsResponse, DiscountResponse, OrderResponse
from app.storage import stats, orders, discount_codes
from app.services.discount_service import generate_discount_code, should_generate_discount


# ---------------------------------------------------------------------------
# Admin Router
# ---------------------------------------------------------------------------
# Provides internal endpoints for store management:
#   - Trigger discount coupon generation
#   - View store-wide stats
#   - List all orders
#   - List all discount codes
#
# In a production system these routes would be protected by admin auth.
# ---------------------------------------------------------------------------

router = APIRouter()


@router.post("/discount/generate", response_model=DiscountResponse)
def generate_coupon():
    """
    Generate a discount coupon if the nth order threshold has been reached.

    Returns the coupon details if eligible, or a message with an empty code
    if the condition is not yet met or already triggered for this interval.
    """
    if not should_generate_discount():
        # Condition not met — return a safe empty response instead of raising
        # an error, so the caller can handle it gracefully
        return DiscountResponse(
            message="Discount generation condition not met",
            code="",
            percentage=0,
        )

    coupon = generate_discount_code()

    return DiscountResponse(
        message="Coupon generated successfully",
        code=coupon.code,
        percentage=coupon.percentage,
    )


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """Return aggregate store statistics across all completed orders."""
    return StatsResponse(
        total_orders=stats.total_orders,
        total_items_sold=stats.total_items_sold,
        total_revenue=stats.total_revenue,
        total_discount_given=stats.total_discount_given,
        discount_codes_generated=stats.discount_codes_generated,
        discount_codes_used=stats.discount_codes_used,
    )


@router.get("/orders", response_model=list[OrderResponse])
def get_orders():
    """Return all placed orders including their status and discount details."""
    return orders


@router.get("/discounts")
def get_discounts():
    """Return all generated discount codes and their usage status."""
    return list(discount_codes.values())