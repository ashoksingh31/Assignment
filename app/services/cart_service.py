from app.models import CartItem
from app.storage import cart


def add_item(product_id, name, price, quantity):
    item = CartItem(
        product_id=product_id,
        name=name,
        price=price,
        quantity=quantity
    )

    cart.append(item)

    return item


def get_cart():
    return cart


def clear_cart():
    cart.clear()


def calculate_subtotal():

    total = 0

    for item in cart:
        total += item.price * item.quantity

    return total