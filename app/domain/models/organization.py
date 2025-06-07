from dataclasses import dataclass
from typing import Optional
from .base import DomainModel

@dataclass
class Organization(DomainModel):
    name: str
    description: Optional[str] = None
    owner_id: int
    menu_table_name: str

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'menu_table_name': self.menu_table_name
        } 