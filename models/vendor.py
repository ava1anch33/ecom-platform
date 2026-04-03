from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Vendor:
    """Vendor represents a merchant in the e-commerce platform."""
    vendor_id: Optional[int] = None
    business_name: str = ''
    average_rating: float = 5.0
    geographical_presence: str = ''
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.business_name:
            raise ValueError("name cannot be empty")
        if not 0 <= self.average_rating <= 5:
            raise ValueError("average_rating must be between 0 and 5")

    def __repr__(self):
        return f"Vendor(id={self.vendor_id}, name='{self.business_name}', rating={self.average_rating})"