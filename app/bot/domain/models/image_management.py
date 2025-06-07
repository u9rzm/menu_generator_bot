from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from datetime import datetime

class ImageType(Enum):
    MENU_ITEM = "menu_item"
    ORGANIZATION = "organization"
    BACKGROUND = "background"
    LOGO = "logo"

@dataclass
class Image:
    organization_id: int
    image_type: ImageType
    file_path: str
    original_filename: str
    uploaded_at: datetime = None
    description: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        if self.uploaded_at is None:
            self.uploaded_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'organization_id': self.organization_id,
            'image_type': self.image_type.value,
            'file_path': self.file_path,
            'original_filename': self.original_filename,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'description': self.description,
            'is_active': self.is_active
        }

@dataclass
class ImageUpload:
    organization_id: int
    image_type: ImageType
    original_filename: str
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
            'image_type': self.image_type.value,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'status': self.status,
            'error_message': self.error_message
        } 