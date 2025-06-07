from typing import Optional
from ..models.menu_management import MenuUpload, MenuFileType
from ..repositories.menu_repository import MenuRepository

class MenuService:
    def __init__(self, repository: MenuRepository):
        self.repository = repository

    async def upload_menu(self, organization_id: int, file_path: str, file_type: MenuFileType) -> MenuUpload:
        """Загружает меню для организации"""
        upload = MenuUpload(
            organization_id=organization_id,
            file_type=file_type,
            file_path=file_path
        )
        return await self.repository.save_upload(upload)

    async def get_menu_upload(self, organization_id: int) -> Optional[MenuUpload]:
        """Получает информацию о загруженном меню"""
        return await self.repository.get_upload(organization_id)

    async def update_upload_status(self, organization_id: int, status: str, error_message: Optional[str] = None) -> MenuUpload:
        """Обновляет статус загрузки меню"""
        upload = await self.repository.get_upload(organization_id)
        if not upload:
            raise ValueError("Menu upload not found")

        upload.status = status
        upload.error_message = error_message
        return await self.repository.update_upload(upload)

    async def delete_menu_upload(self, organization_id: int) -> bool:
        """Удаляет загруженное меню"""
        return await self.repository.delete_upload(organization_id) 