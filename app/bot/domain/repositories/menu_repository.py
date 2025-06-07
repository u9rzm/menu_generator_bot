from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.menu_management import MenuUpload

class MenuRepository(ABC):
    @abstractmethod
    async def save_upload(self, menu_upload: MenuUpload) -> MenuUpload:
        pass

    @abstractmethod
    async def get_upload(self, organization_id: int) -> Optional[MenuUpload]:
        pass

    @abstractmethod
    async def update_upload(self, menu_upload: MenuUpload) -> MenuUpload:
        pass

    @abstractmethod
    async def delete_upload(self, organization_id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_uploads(self) -> List[MenuUpload]:
        pass 