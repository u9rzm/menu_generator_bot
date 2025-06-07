from typing import Optional
from ...domain.services.organization_service import OrganizationService
from ...domain.models.organization_creation import OrganizationCreation

class CreateOrganizationUseCase:
    def __init__(self, organization_service: OrganizationService):
        self.organization_service = organization_service

    async def execute(self, user_id: int) -> OrganizationCreation:
        """Начинает процесс создания организации"""
        return await self.organization_service.start_creation(user_id)

    async def set_name(self, user_id: int, name: str) -> OrganizationCreation:
        """Устанавливает имя организации"""
        return await self.organization_service.update_name(user_id, name)

    async def set_description(self, user_id: int, description: str) -> OrganizationCreation:
        """Устанавливает описание организации"""
        return await self.organization_service.update_description(user_id, description)

    async def upload_menu(self, user_id: int, menu_file: str) -> OrganizationCreation:
        """Загружает меню"""
        return await self.organization_service.add_menu_file(user_id, menu_file)

    async def upload_image(self, user_id: int, image_path: str) -> OrganizationCreation:
        """Загружает изображение"""
        return await self.organization_service.add_image(user_id, image_path)

    async def complete(self, user_id: int) -> OrganizationCreation:
        """Завершает создание организации"""
        return await self.organization_service.complete_creation(user_id) 