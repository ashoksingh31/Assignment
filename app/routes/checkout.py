from fastapi import APIRouter, HTTPException

from app.schemas import CheckoutRequest, CheckoutResponse
from app.services.checkout_service import checkout


# ---------------------------------------------------------------------------
# Checkout Router
# ---------------------------------------------------------------------------
# Single endpoint that orchestrates the full order placement flow.
# All business logic (discount validation, stats update, cart clear)
# is handled inside checkout_service.py.
# ---------------------------------------------------------------------------

router = APIRouter()


@router.post("", response_model=CheckoutResponse)
def checkout_cart(request: CheckoutRequest):
    """
    Place an order from the current cart.

    Optionally accepts a discount_code. If provided, the code is validated
    and the discount is applied before the order is confirmed.

    Raises 400 if:
      - The cart is empty
      - The discount code is invalid or already used
    """
    try:
        order = checkout(request.discount_code)

        return CheckoutResponse(
            message="Order placed successfully",
            order_id=order.order_id,
            subtotal=order.subtotal,
            discount=order.discount,
            total=order.total,
            status=order.status,
        )

    except ValueError as e:
        # ValueError is raised by the service layer for known business rule failures
        raise HTTPException(status_code=400, detail=str(e))