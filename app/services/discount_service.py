import secrets
import string

from app.models import DiscountCode
from app.storage import discount_codes, stats, ORDER_INTERVAL, DISCOUNT_PERCENTAGE


# ---------------------------------------------------------------------------
# Discount Service
# ---------------------------------------------------------------------------
# Handles coupon generation, validation, and redemption.
#
# Discount logic:
#   - A coupon is eligible to be generated every nth order (ORDER_INTERVAL)
#   - `last_discount_order` tracks which order count last triggered a coupon,
#     preventing the admin endpoint from generating duplicates at the same interval
#   - Coupons are single-use; `used` is flipped to True on redemption
# ---------------------------------------------------------------------------


def _generate_code(length: int = 8) -> str:
    """
    Generate a random alphanumeric coupon string.

    Uses `secrets` instead of `random` for cryptographic safety —
    important so coupon codes cannot be predicted or brute-forced.
    """
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def should_generate_discount() -> bool:
    """
    Return True if a new discount coupon is eligible to be generated.

    Conditions that must all be true:
      1. At least one order has been placed
      2. Total orders is a multiple of ORDER_INTERVAL (e.g. 3, 6, 9...)
      3. A coupon has not already been issued for this exact order count
         (prevents duplicate coupons if the admin endpoint is called twice)
    """
    current_orders = stats.total_orders

    return (
        current_orders > 0
        and current_orders % ORDER_INTERVAL == 0
        and stats.last_discount_order != current_orders
    )


def generate_discount_code() -> DiscountCode:
    """
    Create a new unique discount coupon and register it in storage.

    Retries code generation on the rare chance of a collision with an
    existing code. Updates stats and records the current order count
    to prevent re-generation at the same interval.

    Returns the newly created DiscountCode.
    """
    code = _generate_code()

    # Collision guard — regenerate until the code is unique
    while code in discount_codes:
        code = _generate_code()

    coupon = DiscountCode(code=code, percentage=DISCOUNT_PERCENTAGE)
    discount_codes[code] = coupon

    stats.discount_codes_generated += 1

    # Record which order count triggered this coupon so should_generate_discount()
    # returns False if the admin endpoint is called again before the next interval
    stats.last_discount_order = stats.total_orders

    return coupon


def validate_discount(code: str) -> DiscountCode | None:
    """
    Look up a discount code and confirm it is valid for use.

    Returns the DiscountCode if valid, or None if:
      - The code does not exist in storage
      - The code has already been used
    """
    if code is None:
        return None

    coupon = discount_codes.get(code)

    if coupon is None:
        return None

    # Reject already-redeemed coupons (single-use policy)
    if coupon.used:
        return None

    return coupon


def mark_discount_used(code: str) -> None:
    """
    Mark a coupon as redeemed and update usage stats.
    Called immediately after a successful discounted checkout.
    """
    coupon = discount_codes.get(code)

    if coupon:
        coupon.used = True
        stats.discount_codes_used += 1