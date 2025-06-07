from typing import Optional
from ...domain.services.menu_service import MenuService
from ...domain.models.menu_management import MenuUpload, MenuFileType

class ManageMenuUseCase:
    def __init__(self, menu_service: MenuService):
        self.menu_service = menu_service

    async def upload_menu(self, organization_id: int, file_path: str, file_type: MenuFileType) -> MenuUpload:
        """Загружает меню для организации"""
        return await self.menu_service.upload_menu(organization_id, file_path, file_type)

    async def get_menu_upload(self, organization_id: int) -> Optional[MenuUpload]:
        """Получает информацию о загруженном меню"""
        return await self.menu_service.get_menu_upload(organization_id)

    async def update_upload_status(self, organization_id: int, status: str, error_message: Optional[str] = None) -> MenuUpload:
        """Обновляет статус загрузки меню"""
        return await self.menu_service.update_upload_status(organization_id, status, error_message)

    async def delete_menu_upload(self, organization_id: int) -> bool:
        """Удаляет загруженное меню"""
        return await self.menu_service.delete_menu_upload(organization_id) 