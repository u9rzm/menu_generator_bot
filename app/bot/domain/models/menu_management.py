from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from datetime import datetime

class MenuFileType(Enum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"

@dataclass
class MenuUpload:
    organization_id: int
    file_type: MenuFileType
    file_path: str
    uploaded_at: datetime = None
    status: str = "pending"
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.uploaded_at is None:
            self.uploaded_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'organization_id': self.organization_id,
            'file_type': self.file_type.value,
            'file_path': self.file_path,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'status': self.status,
            'error_message': self.error_message
        } 