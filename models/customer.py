from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer class"""
    customer_id: Optional[int] = None
    first_name: str = ''
    contact_number: str = ''
    shipping_address: str = ''

    def __post_init__(self):
        if not self.contact_number or not self.shipping_address or not self.first_name:
            raise ValueError("contact_number, shipping_address and first_name cannot be empty")

    def __repr__(self):
        return f"Customer(id={self.customer_id},name={self.first_name}, contact='{self.contact_number}, address='{self.shipping_address}')"