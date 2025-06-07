import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from app.bot.domain.models.qr_code import QRCode, QRCodeType
from app.bot.domain.services.qr_code_service import QRCodeService
from app.bot.domain.exceptions import EntityNotFoundError

@pytest.fixture
def mock_repository():
    """Create a mock repository for testing"""
    return Mock()

@pytest.fixture
def qr_code_service(mock_repository):
    """Create a QR code service with a mock repository"""
    return QRCodeService(mock_repository)

@pytest.mark.asyncio
async def test_generate_qr_code(qr_code_service, mock_repository):
    """Test generating a QR code"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    content = "https://example.com/menu"
    expires_in_days = 30
    
    expected_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content,
        file_path="/path/to/qr.png",
        expires_at=datetime.now() + timedelta(days=expires_in_days)
    )
    
    mock_repository.save_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await qr_code_service.generate_qr_code(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content,
        expires_in_days=expires_in_days
    )
    
    # Assert
    assert result == expected_qr_code
    mock_repository.save_qr_code.assert_called_once()

@pytest.mark.asyncio
async def test_generate_qr_code_without_expiry(qr_code_service, mock_repository):
    """Test generating a QR code without expiration"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    content = "https://example.com/menu"
    
    expected_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content,
        file_path="/path/to/qr.png"
    )
    
    mock_repository.save_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await qr_code_service.generate_qr_code(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content
    )
    
    # Assert
    assert result == expected_qr_code
    assert result.expires_at is None
    mock_repository.save_qr_code.assert_called_once()

@pytest.mark.asyncio
async def test_get_qr_code(qr_code_service, mock_repository):
    """Test getting a QR code"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    expected_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    mock_repository.get_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await qr_code_service.get_qr_code(organization_id, qr_type)
    
    # Assert
    assert result == expected_qr_code
    mock_repository.get_qr_code.assert_called_once_with(organization_id, qr_type)

@pytest.mark.asyncio
async def test_get_qr_code_not_found(qr_code_service, mock_repository):
    """Test getting a non-existent QR code"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    mock_repository.get_qr_code = AsyncMock(return_value=None)
    
    # Act
    result = await qr_code_service.get_qr_code(organization_id, qr_type)
    
    # Assert
    assert result is None
    mock_repository.get_qr_code.assert_called_once_with(organization_id, qr_type)

@pytest.mark.asyncio
async def test_get_all_qr_codes(qr_code_service, mock_repository):
    """Test getting all QR codes"""
    # Arrange
    organization_id = 1
    
    expected_qr_codes = [
        QRCode(
            organization_id=organization_id,
            qr_type=QRCodeType.MENU,
            content="https://example.com/menu",
            file_path="/path/to/qr1.png"
        ),
        QRCode(
            organization_id=organization_id,
            qr_type=QRCodeType.ORGANIZATION,
            content="https://example.com/org",
            file_path="/path/to/qr2.png"
        )
    ]
    
    mock_repository.get_all_qr_codes = AsyncMock(return_value=expected_qr_codes)
    
    # Act
    result = await qr_code_service.get_all_qr_codes(organization_id)
    
    # Assert
    assert result == expected_qr_codes
    mock_repository.get_all_qr_codes.assert_called_once_with(organization_id)

@pytest.mark.asyncio
async def test_get_active_qr_codes(qr_code_service, mock_repository):
    """Test getting active QR codes"""
    # Arrange
    organization_id = 1
    
    expected_qr_codes = [
        QRCode(
            organization_id=organization_id,
            qr_type=QRCodeType.MENU,
            content="https://example.com/menu",
            file_path="/path/to/qr1.png",
            is_active=True
        ),
        QRCode(
            organization_id=organization_id,
            qr_type=QRCodeType.ORGANIZATION,
            content="https://example.com/org",
            file_path="/path/to/qr2.png",
            is_active=True
        )
    ]
    
    mock_repository.get_active_qr_codes = AsyncMock(return_value=expected_qr_codes)
    
    # Act
    result = await qr_code_service.get_active_qr_codes(organization_id)
    
    # Assert
    assert result == expected_qr_codes
    mock_repository.get_active_qr_codes.assert_called_once_with(organization_id)

@pytest.mark.asyncio
async def test_deactivate_qr_code(qr_code_service, mock_repository):
    """Test deactivating a QR code"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    existing_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        is_active=True
    )
    
    expected_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        is_active=False
    )
    
    mock_repository.get_qr_code = AsyncMock(return_value=existing_qr_code)
    mock_repository.update_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await qr_code_service.deactivate_qr_code(organization_id, qr_type)
    
    # Assert
    assert result == expected_qr_code
    assert result.is_active is False
    mock_repository.get_qr_code.assert_called_once_with(organization_id, qr_type)
    mock_repository.update_qr_code.assert_called_once()

@pytest.mark.asyncio
async def test_deactivate_qr_code_not_found(qr_code_service, mock_repository):
    """Test deactivating a non-existent QR code"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    mock_repository.get_qr_code = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(ValueError):
        await qr_code_service.deactivate_qr_code(organization_id, qr_type)
    
    mock_repository.get_qr_code.assert_called_once_with(organization_id, qr_type)
    mock_repository.update_qr_code.assert_not_called() 