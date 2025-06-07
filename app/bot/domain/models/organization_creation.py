from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
from datetime import datetime

class OrganizationCreationStatus(Enum):
    INITIALIZED = "initialized"
    NAME_PROVIDED = "name_provided"
    DESCRIPTION_PROVIDED = "description_provided"
    MENU_UPLOADED = "menu_uploaded"
    IMAGES_UPLOADED = "images_uploaded"
    COMPLETED = "completed"

@dataclass
class OrganizationCreation:
    user_id: int
    status: OrganizationCreationStatus
    name: Optional[str] = None
    description: Optional[str] = None
    menu_file: Optional[str] = None
    images: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.images is None:
            self.images = []

    def update_status(self, new_status: OrganizationCreationStatus):
        self.status = new_status
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'status': self.status.value,
            'name': self.name,
            'description': self.description,
            'menu_file': self.menu_file,
            'images': self.images,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 