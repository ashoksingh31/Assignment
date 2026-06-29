# ---------------------------------------------------------------------------
# Test Helpers
# ---------------------------------------------------------------------------
# Reusable shortcuts for common test setup actions.
# Using helpers keeps test bodies focused on assertions, not boilerplate.
# ---------------------------------------------------------------------------


def add_keyboard(client, quantity: int):
    """
    Add a Keyboard (product_id=1, price=1000) to the cart.
    Used as a standard product across tests to keep setup consistent.
    """
    return client.post(
        "/cart/items",
        json={
            "product_id": 1,
            "name": "Keyboard",
            "price": 1000,
            "quantity": quantity,
        },
    )


def add_item(client, product_id: int, name: str, price: float, quantity: int):
    """
    Add any product to the cart.
    Use this when a test needs a product other than the default Keyboard.
    """
    return client.post(
        "/cart/items",
        json={
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
        },
    )