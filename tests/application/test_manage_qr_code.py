import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from app.bot.domain.models.qr_code import QRCode, QRCodeType
from app.bot.application.use_cases.manage_qr_code import ManageQRCodeUseCase
from app.bot.domain.exceptions import EntityNotFoundError

@pytest.fixture
def mock_qr_code_service():
    """Create a mock QR code service for testing"""
    return Mock()

@pytest.fixture
def manage_qr_code_use_case(mock_qr_code_service):
    """Create a manage QR code use case with a mock service"""
    return ManageQRCodeUseCase(mock_qr_code_service)

@pytest.mark.asyncio
async def test_generate_qr_code(manage_qr_code_use_case, mock_qr_code_service):
    """Test generating a QR code through the use case"""
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
    
    mock_qr_code_service.generate_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await manage_qr_code_use_case.generate_qr_code(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content,
        expires_in_days=expires_in_days
    )
    
    # Assert
    assert result == expected_qr_code
    mock_qr_code_service.generate_qr_code.assert_called_once_with(
        organization_id=organization_id,
        qr_type=qr_type,
        content=content,
        expires_in_days=expires_in_days
    )

@pytest.mark.asyncio
async def test_get_qr_code(manage_qr_code_use_case, mock_qr_code_service):
    """Test getting a QR code through the use case"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    expected_qr_code = QRCode(
        organization_id=organization_id,
        qr_type=qr_type,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    mock_qr_code_service.get_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await manage_qr_code_use_case.get_qr_code(organization_id, qr_type)
    
    # Assert
    assert result == expected_qr_code
    mock_qr_code_service.get_qr_code.assert_called_once_with(organization_id, qr_type)

@pytest.mark.asyncio
async def test_get_qr_code_not_found(manage_qr_code_use_case, mock_qr_code_service):
    """Test getting a non-existent QR code through the use case"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    mock_qr_code_service.get_qr_code = AsyncMock(return_value=None)
    
    # Act
    result = await manage_qr_code_use_case.get_qr_code(organization_id, qr_type)
    
    # Assert
    assert result is None
    mock_qr_code_service.get_qr_code.assert_called_once_with(organization_id, qr_type)

@pytest.mark.asyncio
async def test_get_all_qr_codes(manage_qr_code_use_case, mock_qr_code_service):
    """Test getting all QR codes through the use case"""
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
    
    mock_qr_code_service.get_all_qr_codes = AsyncMock(return_value=expected_qr_codes)
    
    # Act
    result = await manage_qr_code_use_case.get_all_qr_codes(organization_id)
    
    # Assert
    assert result == expected_qr_codes
    mock_qr_code_service.get_all_qr_codes.assert_called_once_with(organization_id)

@pytest.mark.asyncio
async def test_get_active_qr_codes(manage_qr_code_use_case, mock_qr_code_service):
    """Test getting active QR codes through the use case"""
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
    
    mock_qr_code_service.get_active_qr_codes = AsyncMock(return_value=expected_qr_codes)
    
    # Act
    result = await manage_qr_code_use_case.get_active_qr_codes(organization_id)
    
    # Assert
    assert result == expected_qr_codes
    mock_qr_code_service.get_active_qr_codes.assert_called_once_with(organization_id)

@pytest.mark.asyncio
async def test_deactivate_qr_code(manage_qr_code_use_case, mock_qr_code_service):
    """Test deactivating a QR code through the use case"""
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
    
    mock_qr_code_service.deactivate_qr_code = AsyncMock(return_value=expected_qr_code)
    
    # Act
    result = await manage_qr_code_use_case.deactivate_qr_code(organization_id, qr_type)
    
    # Assert
    assert result == expected_qr_code
    assert result.is_active is False
    mock_qr_code_service.deactivate_qr_code.assert_called_once_with(organization_id, qr_type)

@pytest.mark.asyncio
async def test_deactivate_qr_code_not_found(manage_qr_code_use_case, mock_qr_code_service):
    """Test deactivating a non-existent QR code through the use case"""
    # Arrange
    organization_id = 1
    qr_type = QRCodeType.MENU
    
    mock_qr_code_service.deactivate_qr_code = AsyncMock(side_effect=ValueError("QR code not found"))
    
    # Act & Assert
    with pytest.raises(ValueError):
        await manage_qr_code_use_case.deactivate_qr_code(organization_id, qr_type)
    
    mock_qr_code_service.deactivate_qr_code.assert_called_once_with(organization_id, qr_type) 