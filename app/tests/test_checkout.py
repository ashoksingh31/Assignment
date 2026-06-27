from app.storage import (
    cart,
    orders,
    stats,
)

from app.services.cart_service import add_item
from app.services.checkout_service import checkout


def setup_function():

    cart.clear()
    orders.clear()

    stats.total_orders = 0
    stats.total_items_sold = 0
    stats.total_revenue = 0
    stats.total_discount_given = 0
    stats.discount_codes_generated = 0
    stats.discount_codes_used = 0
    stats.last_discount_order = 0


def test_checkout():

    add_item(
        1,
        "Laptop",
        50000,
        1,
    )

    order = checkout()

    assert order.total == 50000

    assert len(cart) == 0

    assert len(orders) == 1