from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CartItem:
    product_id: int
    name: str
    price: float
    quantity: int


@dataclass
class DiscountCode:
    code: str
    percentage: int
    used: bool = False


@dataclass
class Order:
    order_id: int
    items: List[CartItem]
    subtotal: float
    discount: float
    total: float
    discount_code: Optional[str] = None