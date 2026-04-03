from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

@dataclass
class Order:
    """Order class"""
    order_id: Optional[int] = None
    customer_id: int = None
    order_date: datetime = field(default_factory=datetime.now)
    total_price: float = 0.0
    status: OrderStatus = OrderStatus.PENDING
    items: List['OrderItem'] = field(default_factory=list) 

    def __post_init__(self):
        if self.total_price < 0:
            raise ValueError("total_price should be non-negative")

    def add_item(self, item: 'OrderItem'):
        self.items.append(item)
        self.total_price += item.price_at_purchase * item.quantity

    def __repr__(self):
        return (f"Order(id={self.order_id}, customer={self.customer_id}, "
                f"status={self.status.value}, total={self.total_price})")