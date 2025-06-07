import pytest
from unittest.mock import Mock, AsyncMock
from app.bot.domain.models.image_management import Image, ImageUpload, ImageType
from app.bot.domain.services.image_service import ImageService
from app.bot.domain.exceptions import EntityNotFoundError

@pytest.fixture
def mock_repository():
    """Create a mock repository for testing"""
    return Mock()

@pytest.fixture
def image_service(mock_repository):
    """Create an image service with a mock repository"""
    return ImageService(mock_repository)

@pytest.mark.asyncio
async def test_upload_image(image_service, mock_repository):
    """Test uploading an image"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    file_path = "/path/to/image.jpg"
    original_filename = "image.jpg"
    
    expected_upload = ImageUpload(
        organization_id=organization_id,
        image_type=image_type,
        file_path=file_path,
        original_filename=original_filename
    )
    
    mock_repository.save_upload = AsyncMock(return_value=expected_upload)
    
    # Act
    result = await image_service.upload_image(
        organization_id=organization_id,
        image_type=image_type,
        file_path=file_path,
        original_filename=original_filename
    )
    
    # Assert
    assert result == expected_upload
    mock_repository.save_upload.assert_called_once()

@pytest.mark.asyncio
async def test_get_image(image_service, mock_repository):
    """Test getting an image"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    
    expected_image = Image(
        organization_id=organization_id,
        image_type=image_type,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg"
    )
    
    mock_repository.get_image = AsyncMock(return_value=expected_image)
    
    # Act
    result = await image_service.get_image(organization_id, image_type)
    
    # Assert
    assert result == expected_image
    mock_repository.get_image.assert_called_once_with(organization_id, image_type)

@pytest.mark.asyncio
async def test_get_image_not_found(image_service, mock_repository):
    """Test getting a non-existent image"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    
    mock_repository.get_image = AsyncMock(return_value=None)
    
    # Act
    result = await image_service.get_image(organization_id, image_type)
    
    # Assert
    assert result is None
    mock_repository.get_image.assert_called_once_with(organization_id, image_type)

@pytest.mark.asyncio
async def test_update_upload_status(image_service, mock_repository):
    """Test updating upload status"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    status = "completed"
    error_message = None
    
    existing_upload = ImageUpload(
        organization_id=organization_id,
        image_type=image_type,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg"
    )
    
    expected_upload = ImageUpload(
        organization_id=organization_id,
        image_type=image_type,
        file_path="/path/to/image.jpg",
        original_filename="image.jpg",
        status=status,
        error_message=error_message
    )
    
    mock_repository.get_upload = AsyncMock(return_value=existing_upload)
    mock_repository.update_upload = AsyncMock(return_value=expected_upload)
    
    # Act
    result = await image_service.update_upload_status(
        organization_id=organization_id,
        image_type=image_type,
        status=status,
        error_message=error_message
    )
    
    # Assert
    assert result == expected_upload
    assert result.status == status
    assert result.error_message == error_message
    mock_repository.get_upload.assert_called_once_with(organization_id, image_type)
    mock_repository.update_upload.assert_called_once()

@pytest.mark.asyncio
async def test_update_upload_status_not_found(image_service, mock_repository):
    """Test updating status of non-existent upload"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    status = "completed"
    
    mock_repository.get_upload = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(ValueError):
        await image_service.update_upload_status(
            organization_id=organization_id,
            image_type=image_type,
            status=status
        )
    
    mock_repository.get_upload.assert_called_once_with(organization_id, image_type)
    mock_repository.update_upload.assert_not_called()

@pytest.mark.asyncio
async def test_delete_image(image_service, mock_repository):
    """Test deleting an image"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    
    mock_repository.delete_image = AsyncMock(return_value=True)
    
    # Act
    result = await image_service.delete_image(organization_id, image_type)
    
    # Assert
    assert result is True
    mock_repository.delete_image.assert_called_once_with(organization_id, image_type)

@pytest.mark.asyncio
async def test_delete_image_not_found(image_service, mock_repository):
    """Test deleting a non-existent image"""
    # Arrange
    organization_id = 1
    image_type = ImageType.MENU_ITEM
    
    mock_repository.delete_image = AsyncMock(return_value=False)
    
    # Act
    result = await image_service.delete_image(organization_id, image_type)
    
    # Assert
    assert result is False
    mock_repository.delete_image.assert_called_once_with(organization_id, image_type) 