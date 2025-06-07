from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict
from datetime import datetime

class ThemeType(Enum):
    MODERN_DARK = "modern-dark"
    MODERN_LIGHT = "modern-light"
    CLASSIC = "classic"
    MINIMAL = "minimal"
    AI_GENERATED = "ai-generated"

@dataclass
class Theme:
    organization_id: int
    theme_type: ThemeType
    css_variables: Optional[Dict[str, str]] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.css_variables is None:
            self.css_variables = {}

    def to_dict(self) -> dict:
        return {
            'organization_id': self.organization_id,
            'theme_type': self.theme_type.value,
            'css_variables': self.css_variables,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 