from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict
from datetime import datetime

class QRCodeType(Enum):
    MENU = "menu"
    ORGANIZATION = "organization"
    PROMOTION = "promotion"

@dataclass
class QRCode:
    organization_id: int
    qr_type: QRCodeType
    content: str
    file_path: str
    created_at: datetime = None
    expires_at: Optional[datetime] = None
    is_active: bool = True
    metadata: Optional[Dict] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        return {
            'organization_id': self.organization_id,
            'qr_type': self.qr_type.value,
            'content': self.content,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'metadata': self.metadata
        } 