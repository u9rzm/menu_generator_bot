import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from telegram import Update, Message, Chat, User, CallbackQuery
from telegram.ext import CallbackContext
from app.bot.domain.models.qr_code import QRCode, QRCodeType
from app.bot.infrastructure.handlers.qr_code_handler import QRCodeHandler
from app.bot.application.use_cases.manage_qr_code import ManageQRCodeUseCase

@pytest.fixture
def mock_use_case():
    """Create a mock QR code use case for testing"""
    return Mock(spec=ManageQRCodeUseCase)

@pytest.fixture
def qr_code_handler(mock_use_case):
    """Create a QR code handler with a mock use case"""
    return QRCodeHandler(mock_use_case)

@pytest.fixture
def mock_update():
    """Create a mock update for testing"""
    update = Mock(spec=Update)
    update.message = Mock(spec=Message)
    update.message.chat = Mock(spec=Chat)
    update.message.chat.id = 123
    update.message.from_user = Mock(spec=User)
    update.message.from_user.id = 456
    return update

@pytest.fixture
def mock_context():
    """Create a mock context for testing"""
    context = Mock(spec=CallbackContext)
    context.bot = Mock()
    return context

@pytest.mark.asyncio
async def test_handle_generate_qr(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling QR code generation command"""
    # Arrange
    mock_update.message.text = "/generate_qr menu https://example.com/menu"
    
    expected_qr_code = QRCode(
        organization_id=456,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    mock_use_case.generate_qr_code = AsyncMock(return_value=expected_qr_code)
    mock_context.bot.send_photo = AsyncMock()
    
    # Act
    await qr_code_handler.handle_generate_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.generate_qr_code.assert_called_once_with(
        organization_id=456,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu"
    )
    mock_context.bot.send_photo.assert_called_once()

@pytest.mark.asyncio
async def test_handle_generate_qr_invalid_type(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling QR code generation with invalid type"""
    # Arrange
    mock_update.message.text = "/generate_qr invalid_type https://example.com/menu"
    mock_context.bot.send_message = AsyncMock()
    
    # Act
    await qr_code_handler.handle_generate_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.generate_qr_code.assert_not_called()
    mock_context.bot.send_message.assert_called_once()
    assert "Invalid QR code type" in mock_context.bot.send_message.call_args[0][1]

@pytest.mark.asyncio
async def test_handle_get_qr(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling get QR code command"""
    # Arrange
    mock_update.message.text = "/get_qr menu"
    
    expected_qr_code = QRCode(
        organization_id=456,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    mock_use_case.get_qr_code = AsyncMock(return_value=expected_qr_code)
    mock_context.bot.send_photo = AsyncMock()
    
    # Act
    await qr_code_handler.handle_get_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.get_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.send_photo.assert_called_once()

@pytest.mark.asyncio
async def test_handle_get_qr_not_found(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling get QR code command when QR code not found"""
    # Arrange
    mock_update.message.text = "/get_qr menu"
    
    mock_use_case.get_qr_code = AsyncMock(return_value=None)
    mock_context.bot.send_message = AsyncMock()
    
    # Act
    await qr_code_handler.handle_get_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.get_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.send_message.assert_called_once()
    assert "QR code not found" in mock_context.bot.send_message.call_args[0][1]

@pytest.mark.asyncio
async def test_handle_delete_qr(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling delete QR code command"""
    # Arrange
    mock_update.message.text = "/delete_qr menu"
    
    mock_use_case.deactivate_qr_code = AsyncMock(return_value=True)
    mock_context.bot.send_message = AsyncMock()
    
    # Act
    await qr_code_handler.handle_delete_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.deactivate_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.send_message.assert_called_once()
    assert "QR code deleted successfully" in mock_context.bot.send_message.call_args[0][1]

@pytest.mark.asyncio
async def test_handle_delete_qr_not_found(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling delete QR code command when QR code not found"""
    # Arrange
    mock_update.message.text = "/delete_qr menu"
    
    mock_use_case.deactivate_qr_code = AsyncMock(side_effect=ValueError("QR code not found"))
    mock_context.bot.send_message = AsyncMock()
    
    # Act
    await qr_code_handler.handle_delete_qr(mock_update, mock_context)
    
    # Assert
    mock_use_case.deactivate_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.send_message.assert_called_once()
    assert "QR code not found" in mock_context.bot.send_message.call_args[0][1]

@pytest.mark.asyncio
async def test_handle_qr_callback_delete(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling QR code callback for delete action"""
    # Arrange
    callback_query = Mock(spec=CallbackQuery)
    callback_query.data = "qr_delete:menu"
    callback_query.from_user = Mock(spec=User)
    callback_query.from_user.id = 456
    mock_update.callback_query = callback_query
    
    mock_use_case.deactivate_qr_code = AsyncMock(return_value=True)
    mock_context.bot.answer_callback_query = AsyncMock()
    mock_context.bot.edit_message_text = AsyncMock()
    
    # Act
    await qr_code_handler.handle_qr_callback(mock_update, mock_context)
    
    # Assert
    mock_use_case.deactivate_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.answer_callback_query.assert_called_once()
    mock_context.bot.edit_message_text.assert_called_once()
    assert "QR code deleted successfully" in mock_context.bot.edit_message_text.call_args[0][1]

@pytest.mark.asyncio
async def test_handle_qr_callback_get(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling QR code callback for get action"""
    # Arrange
    callback_query = Mock(spec=CallbackQuery)
    callback_query.data = "qr_get:menu"
    callback_query.from_user = Mock(spec=User)
    callback_query.from_user.id = 456
    mock_update.callback_query = callback_query
    
    expected_qr_code = QRCode(
        organization_id=456,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    mock_use_case.get_qr_code = AsyncMock(return_value=expected_qr_code)
    mock_context.bot.answer_callback_query = AsyncMock()
    mock_context.bot.send_photo = AsyncMock()
    
    # Act
    await qr_code_handler.handle_qr_callback(mock_update, mock_context)
    
    # Assert
    mock_use_case.get_qr_code.assert_called_once_with(456, QRCodeType.MENU)
    mock_context.bot.answer_callback_query.assert_called_once()
    mock_context.bot.send_photo.assert_called_once()

@pytest.mark.asyncio
async def test_handle_qr_callback_invalid_action(qr_code_handler, mock_use_case, mock_update, mock_context):
    """Test handling QR code callback with invalid action"""
    # Arrange
    callback_query = Mock(spec=CallbackQuery)
    callback_query.data = "qr_invalid:menu"
    callback_query.from_user = Mock(spec=User)
    callback_query.from_user.id = 456
    mock_update.callback_query = callback_query
    
    mock_context.bot.answer_callback_query = AsyncMock()
    
    # Act
    await qr_code_handler.handle_qr_callback(mock_update, mock_context)
    
    # Assert
    mock_use_case.deactivate_qr_code.assert_not_called()
    mock_use_case.get_qr_code.assert_not_called()
    mock_context.bot.answer_callback_query.assert_called_once()
    assert "Invalid action" in mock_context.bot.answer_callback_query.call_args[0][1] 