from typing import Optional, Dict, List
from ...domain.services.theme_service import ThemeService
from ...domain.models.theme_management import Theme, ThemeType

class ManageThemeUseCase:
    def __init__(self, theme_service: ThemeService):
        self.theme_service = theme_service

    async def set_theme(self, organization_id: int, theme_type: ThemeType, css_variables: Optional[Dict[str, str]] = None) -> Theme:
        """Устанавливает тему для организации"""
        return await self.theme_service.set_theme(organization_id, theme_type, css_variables)

    async def get_theme(self, organization_id: int) -> Optional[Theme]:
        """Получает тему организации"""
        return await self.theme_service.get_theme(organization_id)

    async def update_theme(self, organization_id: int, theme_type: ThemeType, css_variables: Optional[Dict[str, str]] = None) -> Theme:
        """Обновляет тему организации"""
        return await self.theme_service.update_theme(organization_id, theme_type, css_variables)

    async def delete_theme(self, organization_id: int) -> bool:
        """Удаляет тему организации"""
        return await self.theme_service.delete_theme(organization_id)

    async def get_all_themes(self) -> List[Theme]:
        """Получает все темы"""
        return await self.theme_service.get_all_themes() 