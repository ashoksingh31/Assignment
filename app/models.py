from dataclasses import dataclass
from typing import List, Optional


# ---------------------------------------------------------------------------
# Domain Models
# ---------------------------------------------------------------------------
# These are internal data structures used by the service layer.
# Pydantic models (schemas.py) handle request/response validation at the API
# boundary. Keeping them separate ensures business logic stays independent
# of the HTTP layer.
# ---------------------------------------------------------------------------


@dataclass
class CartItem:
    """Represents a single product line in the shopping cart."""

    product_id: int
    name: str
    price: float       # Unit price at the time of adding to cart
    quantity: int      # Total quantity for this product line


@dataclass
class DiscountCode:
    """Represents a generated discount coupon."""

    code: str          # Unique alphanumeric coupon string
    percentage: int    # Discount percentage to apply at checkout (e.g. 10 = 10%)
    used: bool = False # Becomes True after first successful checkout; prevents reuse


@dataclass
class Order:
    """Represents a completed order after a successful checkout."""

    order_id: int
    items: List[CartItem]       # Snapshot of cart at time of checkout
    subtotal: float             # Total before discount
    discount: float             # Discount amount applied (0 if no coupon used)
    total: float                # Final amount charged (subtotal - discount)
    discount_code: Optional[str] = None  # Coupon code used, if any
    status: str = "confirmed"   # Order lifecycle status; supports future transitions


@dataclass
class Stats:
    """Tracks store-wide aggregate statistics across all orders."""

    total_orders: int = 0               # Number of successfully placed orders
    total_items_sold: int = 0           # Sum of all item quantities across orders
    total_revenue: float = 0            # Sum of all order totals (after discount)
    total_discount_given: float = 0     # Sum of all discount amounts applied
    discount_codes_generated: int = 0   # Total coupons created by the admin endpoint
    discount_codes_used: int = 0        # Total coupons redeemed at checkout
    last_discount_order: int = 0        # Order count at which last coupon was issued; prevents issuing duplicate coupons at the same nth interval