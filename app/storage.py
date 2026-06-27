from app.models import CartItem, Order, DiscountCode


cart: list[CartItem] = []

orders: list[Order] = []

discount_codes: dict[str, DiscountCode] = {}

stats = {
    "total_orders": 0,
    "total_items_sold": 0,
    "total_revenue": 0.0,
    "total_discount_given": 0.0,
    "discount_codes_generated": 0,
    "discount_codes_used": 0
}


ORDER_INTERVAL = 3
DISCOUNT_PERCENTAGE = 10