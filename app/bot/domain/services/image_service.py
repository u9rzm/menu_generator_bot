from typing import Optional, List, Dict
from ..models.image_management import Image, ImageUpload, ImageType
from ..repositories.image_repository import ImageRepository

class ImageService:
    def __init__(self, image_repository: ImageRepository):
        self._image_repository = image_repository

    async def upload_image(self, organization_id: int, image_type: ImageType, 
                          file_path: str, original_filename: str) -> ImageUpload:
        """Upload a new image for an organization"""
        upload = ImageUpload(
            organization_id=organization_id,
            image_type=image_type,
            file_path=file_path,
            original_filename=original_filename
        )
        return await self._image_repository.save_upload(upload)

    async def get_image(self, organization_id: int, image_type: ImageType) -> Optional[Image]:
        """Get an image for an organization"""
        return await self._image_repository.get_image(organization_id, image_type)

    async def get_all_images(self, organization_id: int) -> List[Image]:
        """Get all images for an organization"""
        return await self._image_repository.get_all_images(organization_id)

    async def update_image(self, image: Image) -> Image:
        """Update an existing image"""
        return await self._image_repository.update_image(image)

    async def delete_image(self, organization_id: int, image_type: ImageType) -> bool:
        """Delete an image"""
        return await self._image_repository.delete_image(organization_id, image_type)

    async def get_upload(self, organization_id: int, image_type: ImageType) -> Optional[ImageUpload]:
        """Get information about an image upload"""
        return await self._image_repository.get_upload(organization_id, image_type)

    async def update_upload_status(self, organization_id: int, image_type: ImageType, 
                                 status: str, error_message: Optional[str] = None) -> ImageUpload:
        """Update the status of an image upload"""
        upload = await self._image_repository.get_upload(organization_id, image_type)
        if not upload:
            raise ValueError(f"No upload found for organization {organization_id} and type {image_type}")
        
        upload.status = status
        upload.error_message = error_message
        return await self._image_repository.update_upload(upload)

    async def delete_upload(self, organization_id: int, image_type: ImageType) -> bool:
        """Delete an image upload"""
        return await self._image_repository.delete_upload(organization_id, image_type) 