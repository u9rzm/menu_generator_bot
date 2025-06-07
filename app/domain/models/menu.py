from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from .base import DomainModel

@dataclass
class Menu(DomainModel):
    name: str
    price: Decimal
    category: str
    description: Optional[str] = None
    subcategory: Optional[str] = None
    is_available: bool = True
    image_url: Optional[str] = None
    organization_id: int

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'name': self.name,
            'price': float(self.price),
            'category': self.category,
            'description': self.description,
            'subcategory': self.subcategory,
            'is_available': self.is_available,
            'image_url': self.image_url,
            'organization_id': self.organization_id
        } 