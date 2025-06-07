from dataclasses import dataclass
from typing import Optional
from .base import DomainModel

@dataclass
class User(DomainModel):
    tid: int  # Telegram ID
    owner: bool = False
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        return {
            **base_dict,
            'tid': self.tid,
            'owner': self.owner,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        } 