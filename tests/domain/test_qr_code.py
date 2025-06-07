import pytest
from datetime import datetime, timedelta
from app.bot.domain.models.qr_code import QRCode, QRCodeType

def test_qr_code_creation():
    """Test QR code creation with required fields"""
    qr_code = QRCode(
        organization_id=1,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png"
    )
    
    assert qr_code.organization_id == 1
    assert qr_code.qr_type == QRCodeType.MENU
    assert qr_code.content == "https://example.com/menu"
    assert qr_code.file_path == "/path/to/qr.png"
    assert qr_code.is_active is True
    assert qr_code.expires_at is None
    assert qr_code.metadata == {}
    assert isinstance(qr_code.created_at, datetime)

def test_qr_code_creation_with_optional_fields():
    """Test QR code creation with optional fields"""
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=30)
    metadata = {"purpose": "menu", "version": "1.0"}
    
    qr_code = QRCode(
        organization_id=1,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        created_at=created_at,
        expires_at=expires_at,
        is_active=False,
        metadata=metadata
    )
    
    assert qr_code.created_at == created_at
    assert qr_code.expires_at == expires_at
    assert qr_code.is_active is False
    assert qr_code.metadata == metadata

def test_qr_code_to_dict():
    """Test QR code to_dict method"""
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=30)
    metadata = {"purpose": "menu", "version": "1.0"}
    
    qr_code = QRCode(
        organization_id=1,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        created_at=created_at,
        expires_at=expires_at,
        is_active=True,
        metadata=metadata
    )
    
    qr_dict = qr_code.to_dict()
    
    assert qr_dict["organization_id"] == 1
    assert qr_dict["qr_type"] == QRCodeType.MENU.value
    assert qr_dict["content"] == "https://example.com/menu"
    assert qr_dict["file_path"] == "/path/to/qr.png"
    assert qr_dict["created_at"] == created_at.isoformat()
    assert qr_dict["expires_at"] == expires_at.isoformat()
    assert qr_dict["is_active"] is True
    assert qr_dict["metadata"] == metadata

def test_qr_code_expired():
    """Test QR code expiration check"""
    created_at = datetime.now()
    expires_at = created_at - timedelta(days=1)  # Expired yesterday
    
    qr_code = QRCode(
        organization_id=1,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        created_at=created_at,
        expires_at=expires_at
    )
    
    assert qr_code.expires_at < datetime.now()

def test_qr_code_not_expired():
    """Test QR code not expired check"""
    created_at = datetime.now()
    expires_at = created_at + timedelta(days=1)  # Expires tomorrow
    
    qr_code = QRCode(
        organization_id=1,
        qr_type=QRCodeType.MENU,
        content="https://example.com/menu",
        file_path="/path/to/qr.png",
        created_at=created_at,
        expires_at=expires_at
    )
    
    assert qr_code.expires_at > datetime.now() 