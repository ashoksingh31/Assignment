from app.models import Order
from app.storage import cart, orders, stats
from app.services.cart_service import calculate_subtotal, clear_cart
from app.services.discount_service import validate_discount, mark_discount_used


# ---------------------------------------------------------------------------
# Checkout Service
# ---------------------------------------------------------------------------
# Orchestrates the full checkout flow:
#   1. Validate cart is not empty
#   2. Calculate subtotal
#   3. Validate and apply discount code (if provided)
#   4. Create and persist the order
#   5. Update store-wide stats
#   6. Clear the cart
# ---------------------------------------------------------------------------


def checkout(discount_code: str = None) -> Order:
    """
    Place an order from the current cart contents.

    Args:
        discount_code: Optional coupon code. If provided and valid, a percentage
                       discount is applied to the subtotal.

    Returns:
        The completed Order object.

    Raises:
        ValueError: If the cart is empty or the discount code is invalid.
    """

    # Guard: cannot checkout with an empty cart
    if len(cart) == 0:
        raise ValueError("Cart is empty")

    subtotal = calculate_subtotal()
    discount_amount = 0.0

    if discount_code:
        coupon = validate_discount(discount_code)

        if coupon is None:
            # Code doesn't exist or has already been used
            raise ValueError("Invalid discount code")

        # Round to 2 decimal places to avoid floating point drift on money values
        discount_amount = round(subtotal * coupon.percentage / 100, 2)

        # Mark coupon as used immediately to prevent reuse in concurrent requests
        mark_discount_used(discount_code)

    total = subtotal - discount_amount

    # Build the order — cart items are copied so the order is a historical snapshot
    order = Order(
        order_id=len(orders) + 1,
        items=cart.copy(),
        subtotal=subtotal,
        discount=discount_amount,
        total=total,
        discount_code=discount_code,
    )

    orders.append(order)

    # ---------------------------------------------------------------------------
    # Update Stats
    # ---------------------------------------------------------------------------
    stats.total_orders += 1
    stats.total_items_sold += sum(item.quantity for item in cart)
    stats.total_revenue += total
    stats.total_discount_given += discount_amount

    # Cart is cleared last so stats can still read from it above
    clear_cart()

    return order