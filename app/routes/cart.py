from fastapi import APIRouter

from app.schemas import AddItemRequest, CartResponse
from app.services.cart_service import add_item, get_cart, calculate_subtotal


# ---------------------------------------------------------------------------
# Cart Router
# ---------------------------------------------------------------------------
# Handles all cart-related endpoints.
# Business logic lives in cart_service.py — routes only handle HTTP concerns.
# ---------------------------------------------------------------------------

router = APIRouter()


@router.post("/items")
def add_item_to_cart(item: AddItemRequest):
    """
    Add a product to the cart.

    If the product already exists (same product_id), quantity is merged.
    Pydantic validates price > 0 and quantity > 0 before this runs.
    """
    cart_item = add_item(
        item.product_id,
        item.name,
        item.price,
        item.quantity,
    )

    return {
        "message": "Item added successfully",
        "item": cart_item,
    }


@router.get("", response_model=CartResponse)
def view_cart():
    """Return all items currently in the cart along with the subtotal."""
    return {
        "items": get_cart(),
        "subtotal": calculate_subtotal(),
    }