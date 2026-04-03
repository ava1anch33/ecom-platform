from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """transaction class"""
    transaction_id: Optional[int] = None
    order_id: int = None
    vendor_id: int = None
    amount: float = 0.0
    transaction_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("amount should greater or equal to 0")

    def __repr__(self):
        return (f"Transaction(id={self.transaction_id}, order={self.order_id}, "
                f"vendor={self.vendor_id}, amount={self.amount})")