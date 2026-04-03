from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderItem:
    """order item detail"""
    order_item_id: Optional[int] = None
    order_id: int = None
    product_id: int = None
    quantity: int = None
    price_at_purchase: float = 0.0

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity should greater than 0")
        if self.price_at_purchase <= 0:
            raise ValueError("price should non-negative")

    def __repr__(self):
        return (f"OrderItem(product_id={self.product_id}, "
                f"qty={self.quantity}, price={self.price_at_purchase})")