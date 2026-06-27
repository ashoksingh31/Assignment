from app.models import Order

from app.storage import (
    cart,
    orders,
    stats,
)

from app.services.cart_service import (
    calculate_subtotal,
    clear_cart,
)

from app.services.discount_service import (
    validate_discount,
    mark_discount_used,
)


def checkout(discount_code=None):

    if len(cart) == 0:
        raise ValueError("Cart is empty")

    subtotal = calculate_subtotal()

    discount_amount = 0

    if discount_code:

        coupon = validate_discount(discount_code)

        if coupon is None:
            raise ValueError("Invalid discount code")

        discount_amount = (
            subtotal * coupon.percentage / 100
        )

        mark_discount_used(discount_code)

    total = subtotal - discount_amount

    order = Order(
        order_id=len(orders) + 1,
        items=cart.copy(),
        subtotal=subtotal,
        discount=discount_amount,
        total=total,
        discount_code=discount_code,
    )

    orders.append(order)

    stats.total_orders += 1

    stats.total_items_sold += sum(
        item.quantity for item in cart
            )

    stats.total_revenue += total

    stats.total_discount_given += discount_amount


    clear_cart()

    return order