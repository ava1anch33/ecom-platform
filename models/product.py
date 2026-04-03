from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    """Product class (max 3 tags)"""
    product_id: Optional[int] = None
    vendor_id: int = None
    name: str = None
    listed_price: float = 0
    stock_quantity: int = 100
    tag1: Optional[str] = None
    tag2: Optional[str] = None
    tag3: Optional[str] = None

    def __post_init__(self):
        if self.listed_price <= 0:
            raise ValueError("price should greater than 0")
        if self.stock_quantity < 0:
            raise ValueError("quantity should be non-negative")

    def get_tags(self) -> list[str]:
        """return a list of non-empty tags"""
        tags = [self.tag1, self.tag2, self.tag3]
        return [tag for tag in tags if tag]

    def __repr__(self):
        return (f"Product(id={self.product_id}, name='{self.name}', "
                f"price={self.listed_price}, stock={self.stock_quantity}, "
                f"vendor_id={self.vendor_id})")