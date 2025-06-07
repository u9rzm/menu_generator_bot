from typing import Optional
from ..models.organization_creation import OrganizationCreation, OrganizationCreationStatus
from ..repositories.organization_creation_repository import OrganizationCreationRepository

class OrganizationService:
    def __init__(self, repository: OrganizationCreationRepository):
        self.repository = repository

    async def start_creation(self, user_id: int) -> OrganizationCreation:
        """Начинает процесс создания организации"""
        existing = await self.repository.get_by_user_id(user_id)
        if existing:
            return existing

        creation = OrganizationCreation(
            user_id=user_id,
            status=OrganizationCreationStatus.INITIALIZED
        )
        return await self.repository.save(creation)

    async def update_name(self, user_id: int, name: str) -> OrganizationCreation:
        """Обновляет имя организации"""
        creation = await self.repository.get_by_user_id(user_id)
        if not creation:
            raise ValueError("Organization creation not found")

        creation.name = name
        creation.update_status(OrganizationCreationStatus.NAME_PROVIDED)
        return await self.repository.update(creation)

    async def update_description(self, user_id: int, description: str) -> OrganizationCreation:
        """Обновляет описание организации"""
        creation = await self.repository.get_by_user_id(user_id)
        if not creation:
            raise ValueError("Organization creation not found")

        creation.description = description
        creation.update_status(OrganizationCreationStatus.DESCRIPTION_PROVIDED)
        return await self.repository.update(creation)

    async def add_menu_file(self, user_id: int, menu_file: str) -> OrganizationCreation:
        """Добавляет файл меню"""
        creation = await self.repository.get_by_user_id(user_id)
        if not creation:
            raise ValueError("Organization creation not found")

        creation.menu_file = menu_file
        creation.update_status(OrganizationCreationStatus.MENU_UPLOADED)
        return await self.repository.update(creation)

    async def add_image(self, user_id: int, image_path: str) -> OrganizationCreation:
        """Добавляет изображение"""
        creation = await self.repository.get_by_user_id(user_id)
        if not creation:
            raise ValueError("Organization creation not found")

        creation.images.append(image_path)
        creation.update_status(OrganizationCreationStatus.IMAGES_UPLOADED)
        return await self.repository.update(creation)

    async def complete_creation(self, user_id: int) -> OrganizationCreation:
        """Завершает процесс создания организации"""
        creation = await self.repository.get_by_user_id(user_id)
        if not creation:
            raise ValueError("Organization creation not found")

        creation.update_status(OrganizationCreationStatus.COMPLETED)
        return await self.repository.update(creation) 