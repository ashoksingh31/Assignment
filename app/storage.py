from app.models import CartItem, Order, DiscountCode, Stats


# ---------------------------------------------------------------------------
# In-Memory Storage
# ---------------------------------------------------------------------------
# All data is stored in plain Python structures for simplicity.
# This is intentional — the assignment does not require persistence.
# The service layer imports these directly; swapping to a database later
# only requires changing the service layer, not the routes.
# ---------------------------------------------------------------------------


# Active shopping cart — holds CartItem objects.
# A single global cart is used since the assignment has no user auth.
cart: list[CartItem] = []

# Completed orders — appended to on every successful checkout.
orders: list[Order] = []

# Discount code registry — keyed by code string for O(1) lookup at checkout.
discount_codes: dict[str, DiscountCode] = {}

# Singleton stats object — updated in place after every checkout.
stats = Stats()


# ---------------------------------------------------------------------------
# Configuration Constants
# ---------------------------------------------------------------------------

# A discount coupon is generated every nth order.
ORDER_INTERVAL = 3

# Percentage discount applied when a valid coupon is used at checkout.
DISCOUNT_PERCENTAGE = 10