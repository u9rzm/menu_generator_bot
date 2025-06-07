from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ThemeType(Enum):
    MODERN_DARK = "modern-dark"
    MODERN_LIGHT = "modern-light"
    CLASSIC = "classic"
    MINIMAL = "minimal"

@dataclass(frozen=True)
class Theme:
    name: ThemeType
    description: Optional[str] = None
    css_variables: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            'name': self.name.value,
            'description': self.description,
            'css_variables': self.css_variables
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Theme':
        return cls(
            name=ThemeType(data['name']),
            description=data.get('description'),
            css_variables=data.get('css_variables')
        ) 