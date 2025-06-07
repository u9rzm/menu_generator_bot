from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.image_management import Image, ImageUpload, ImageType

class ImageRepository(ABC):
    @abstractmethod
    async def save_image(self, image: Image) -> Image:
        pass

    @abstractmethod
    async def get_image(self, organization_id: int, image_type: ImageType) -> Optional[Image]:
        pass

    @abstractmethod
    async def get_all_images(self, organization_id: int) -> List[Image]:
        pass

    @abstractmethod
    async def update_image(self, image: Image) -> Image:
        pass

    @abstractmethod
    async def delete_image(self, organization_id: int, image_type: ImageType) -> bool:
        pass

    @abstractmethod
    async def save_upload(self, upload: ImageUpload) -> ImageUpload:
        pass

    @abstractmethod
    async def get_upload(self, organization_id: int, image_type: ImageType) -> Optional[ImageUpload]:
        pass

    @abstractmethod
    async def update_upload(self, upload: ImageUpload) -> ImageUpload:
        pass

    @abstractmethod
    async def delete_upload(self, organization_id: int, image_type: ImageType) -> bool:
        pass 