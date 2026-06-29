from app.models import CartItem
from app.storage import cart


# ---------------------------------------------------------------------------
# Cart Service
# ---------------------------------------------------------------------------
# Handles all cart mutations and queries.
# Routes should never touch the cart list directly — always go through here.
# ---------------------------------------------------------------------------


def add_item(product_id: int, name: str, price: float, quantity: int) -> CartItem:
    """
    Add a product to the cart.

    If the product already exists (matched by product_id), its quantity is
    increased. The original price is kept — a re-add with a different price
    does not update the price. This is intentional; see DECISIONS.md.

    Returns the updated or newly created CartItem.
    """
    for item in cart:
        if item.product_id == product_id:
            # Merge: increment quantity on existing line item
            item.quantity += quantity
            return item

    # New product — create a fresh line item and append to cart
    new_item = CartItem(
        product_id=product_id,
        name=name,
        price=price,
        quantity=quantity,
    )
    cart.append(new_item)
    return new_item


def get_cart() -> list[CartItem]:
    """Return the current cart contents."""
    return cart


def clear_cart() -> None:
    """Empty the cart. Called after a successful checkout."""
    cart.clear()


def calculate_subtotal() -> float:
    """
    Return the total price of all items in the cart.
    Computed as sum of (unit price × quantity) across all line items.
    """
    return sum(item.price * item.quantity for item in cart)