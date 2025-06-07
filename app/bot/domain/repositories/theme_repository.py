from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.theme_management import Theme

class ThemeRepository(ABC):
    @abstractmethod
    async def save_theme(self, theme: Theme) -> Theme:
        pass

    @abstractmethod
    async def get_theme(self, organization_id: int) -> Optional[Theme]:
        pass

    @abstractmethod
    async def update_theme(self, theme: Theme) -> Theme:
        pass

    @abstractmethod
    async def delete_theme(self, organization_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_themes(self) -> List[Theme]:
        pass 