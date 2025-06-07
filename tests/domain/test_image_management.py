import pytest
from datetime import datetime
from app.bot.domain.models.image_management import Image, ImageUpload, ImageType

def test_image_creation():
    """Test image creation with required fields"""
    image = Image(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg"
    )
    
    assert image.organization_id == 1
    assert image.image_type == ImageType.MENU_ITEM
    assert image.file_path == "/path/to/image.jpg"
    assert image.original_filename == "image.jpg"
    assert image.is_active is True
    assert image.description is None
    assert isinstance(image.uploaded_at, datetime)

def test_image_creation_with_optional_fields():
    """Test image creation with optional fields"""
    description = "Test image"
    uploaded_at = datetime.now()
    
    image = Image(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg",
        description=description,
        uploaded_at=uploaded_at,
        is_active=False
    )
    
    assert image.description == description
    assert image.uploaded_at == uploaded_at
    assert image.is_active is False

def test_image_to_dict():
    """Test image to_dict method"""
    uploaded_at = datetime.now()
    image = Image(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg",
        description="Test image",
        uploaded_at=uploaded_at,
        is_active=True
    )
    
    image_dict = image.to_dict()
    
    assert image_dict["organization_id"] == 1
    assert image_dict["image_type"] == ImageType.MENU_ITEM.value
    assert image_dict["file_path"] == "/path/to/image.jpg"
    assert image_dict["original_filename"] == "image.jpg"
    assert image_dict["description"] == "Test image"
    assert image_dict["uploaded_at"] == uploaded_at.isoformat()
    assert image_dict["is_active"] is True

def test_image_upload_creation():
    """Test image upload creation"""
    upload = ImageUpload(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg"
    )
    
    assert upload.organization_id == 1
    assert upload.image_type == ImageType.MENU_ITEM
    assert upload.file_path == "/path/to/image.jpg"
    assert upload.original_filename == "image.jpg"
    assert upload.status == "pending"
    assert upload.error_message is None
    assert isinstance(upload.uploaded_at, datetime)

def test_image_upload_creation_with_status():
    """Test image upload creation with status and error message"""
    upload = ImageUpload(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg",
        status="error",
        error_message="Failed to process image"
    )
    
    assert upload.status == "error"
    assert upload.error_message == "Failed to process image"

def test_image_upload_to_dict():
    """Test image upload to_dict method"""
    uploaded_at = datetime.now()
    upload = ImageUpload(
        organization_id=1,
        image_type=ImageType.MENU_ITEM,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg",
        uploaded_at=uploaded_at,
        status="completed",
        error_message=None
    )
    
    upload_dict = upload.to_dict()
    
    assert upload_dict["organization_id"] == 1
    assert upload_dict["image_type"] == ImageType.MENU_ITEM.value
    assert upload_dict["file_path"] == "/path/to/image.jpg"
    assert upload_dict["original_filename"] == "image.jpg"
    assert upload_dict["uploaded_at"] == uploaded_at.isoformat()
    assert upload_dict["status"] == "completed"
    assert upload_dict["error_message"] is None 