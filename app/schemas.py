from typing import Optional, List
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
# Used exclusively at the API boundary for request validation and response
# serialisation. Internal business logic uses dataclasses from models.py.
#
# Keeping schemas separate from domain models means API contract changes
# (e.g. renaming a field) don't touch core business logic.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Cart Schemas
# ---------------------------------------------------------------------------

class AddItemRequest(BaseModel):
    """Payload for adding a product to the cart."""

    product_id: int
    name: str
    price: float = Field(gt=0)   # Must be positive; validated by Pydantic before hitting the service
    quantity: int = Field(gt=0)  # Must be at least 1


class CartItemResponse(BaseModel):
    """Single product line returned in cart responses."""

    product_id: int
    name: str
    price: float
    quantity: int


class CartResponse(BaseModel):
    """Full cart state including all line items and running subtotal."""

    items: List[CartItemResponse]
    subtotal: float


# ---------------------------------------------------------------------------
# Checkout Schemas
# ---------------------------------------------------------------------------

class CheckoutRequest(BaseModel):
    """Payload for placing an order. Discount code is optional."""

    discount_code: Optional[str] = None


class CheckoutResponse(BaseModel):
    """Order confirmation returned after a successful checkout."""

    message: str
    order_id: int
    subtotal: float   # Total before discount
    discount: float   # Amount deducted (0 if no coupon used)
    total: float      # Final charged amount (subtotal - discount)
    status: str       # Order lifecycle status (e.g. "confirmed")


# ---------------------------------------------------------------------------
# Admin Schemas
# ---------------------------------------------------------------------------

class DiscountResponse(BaseModel):
    """Response from the discount code generation endpoint."""

    message: str
    code: str        # Empty string if generation condition was not met
    percentage: int  # Discount percentage (0 if condition not met)


class OrderResponse(BaseModel):
    """Order summary returned by the admin orders list endpoint."""

    order_id: int
    subtotal: float
    discount: float
    total: float
    status: str
    discount_code: Optional[str] = None  # Null if no coupon was applied


class StatsResponse(BaseModel):
    """Aggregate store statistics returned by the admin stats endpoint."""

    total_orders: int
    total_items_sold: int
    total_revenue: float
    total_discount_given: float
    discount_codes_generated: int
    discount_codes_used: int