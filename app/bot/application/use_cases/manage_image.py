from typing import Optional, List, Dict
from ...domain.models.image_management import Image, ImageUpload, ImageType
from ...domain.services.image_service import ImageService

class ManageImageUseCase:
    def __init__(self, image_service: ImageService):
        self._image_service = image_service

    async def upload_image(self, organization_id: int, image_type: ImageType, 
                          file_path: str, original_filename: str) -> ImageUpload:
        """Upload a new image for an organization"""
        return await self._image_service.upload_image(
            organization_id=organization_id,
            image_type=image_type,
            file_path=file_path,
            original_filename=original_filename
        )

    async def get_image(self, organization_id: int, image_type: ImageType) -> Optional[Image]:
        """Get an image for an organization"""
        return await self._image_service.get_image(organization_id, image_type)

    async def get_all_images(self, organization_id: int) -> List[Image]:
        """Get all images for an organization"""
        return await self._image_service.get_all_images(organization_id)

    async def update_image(self, image: Image) -> Image:
        """Update an existing image"""
        return await self._image_service.update_image(image)

    async def delete_image(self, organization_id: int, image_type: ImageType) -> bool:
        """Delete an image"""
        return await self._image_service.delete_image(organization_id, image_type)

    async def get_upload(self, organization_id: int, image_type: ImageType) -> Optional[ImageUpload]:
        """Get information about an image upload"""
        return await self._image_service.get_upload(organization_id, image_type)

    async def update_upload_status(self, organization_id: int, image_type: ImageType, 
                                 status: str, error_message: Optional[str] = None) -> ImageUpload:
        """Update the status of an image upload"""
        return await self._image_service.update_upload_status(
            organization_id=organization_id,
            image_type=image_type,
            status=status,
            error_message=error_message
        )

    async def delete_upload(self, organization_id: int, image_type: ImageType) -> bool:
        """Delete an image upload"""
        return await self._image_service.delete_upload(organization_id, image_type) 