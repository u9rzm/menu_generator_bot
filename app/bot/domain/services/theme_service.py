from typing import Optional, Dict, List
from ..models.theme_management import Theme, ThemeType
from ..repositories.theme_repository import ThemeRepository

class ThemeService:
    def __init__(self, repository: ThemeRepository):
        self.repository = repository

    async def set_theme(self, organization_id: int, theme_type: ThemeType, css_variables: Optional[Dict[str, str]] = None) -> Theme:
        """Устанавливает тему для организации"""
        theme = Theme(
            organization_id=organization_id,
            theme_type=theme_type,
            css_variables=css_variables
        )
        return await self.repository.save_theme(theme)

    async def get_theme(self, organization_id: int) -> Optional[Theme]:
        """Получает тему организации"""
        return await self.repository.get_theme(organization_id)

    async def update_theme(self, organization_id: int, theme_type: ThemeType, css_variables: Optional[Dict[str, str]] = None) -> Theme:
        """Обновляет тему организации"""
        theme = await self.repository.get_theme(organization_id)
        if not theme:
            raise ValueError("Theme not found")

        theme.theme_type = theme_type
        if css_variables is not None:
            theme.css_variables = css_variables
        return await self.repository.update_theme(theme)

    async def delete_theme(self, organization_id: int) -> bool:
        """Удаляет тему организации"""
        return await self.repository.delete_theme(organization_id)

    async def get_all_themes(self) -> List[Theme]:
        """Получает все темы"""
        return await self.repository.get_all_themes() 