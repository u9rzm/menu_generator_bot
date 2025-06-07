from typing import Optional, List, Dict
from datetime import datetime, timedelta
from ..models.qr_code import QRCode, QRCodeType
from ..repositories.qr_code_repository import QRCodeRepository

class QRCodeService:
    def __init__(self, qr_code_repository: QRCodeRepository):
        self._qr_code_repository = qr_code_repository

    async def generate_qr_code(self, organization_id: int, qr_type: QRCodeType, 
                             content: str, expires_in_days: Optional[int] = None,
                             metadata: Optional[Dict] = None) -> QRCode:
        """Generate a new QR code for an organization"""
        expires_at = None
        if expires_in_days is not None:
            expires_at = datetime.now() + timedelta(days=expires_in_days)

        qr_code = QRCode(
            organization_id=organization_id,
            qr_type=qr_type,
            content=content,
            file_path="",  # Will be set by the infrastructure layer
            expires_at=expires_at,
            metadata=metadata
        )
        return await self._qr_code_repository.save_qr_code(qr_code)

    async def get_qr_code(self, organization_id: int, qr_type: QRCodeType) -> Optional[QRCode]:
        """Get a QR code for an organization"""
        return await self._qr_code_repository.get_qr_code(organization_id, qr_type)

    async def get_all_qr_codes(self, organization_id: int) -> List[QRCode]:
        """Get all QR codes for an organization"""
        return await self._qr_code_repository.get_all_qr_codes(organization_id)

    async def get_active_qr_codes(self, organization_id: int) -> List[QRCode]:
        """Get all active QR codes for an organization"""
        return await self._qr_code_repository.get_active_qr_codes(organization_id)

    async def update_qr_code(self, qr_code: QRCode) -> QRCode:
        """Update an existing QR code"""
        return await self._qr_code_repository.update_qr_code(qr_code)

    async def delete_qr_code(self, organization_id: int, qr_type: QRCodeType) -> bool:
        """Delete a QR code"""
        return await self._qr_code_repository.delete_qr_code(organization_id, qr_type)

    async def deactivate_qr_code(self, organization_id: int, qr_type: QRCodeType) -> QRCode:
        """Deactivate a QR code"""
        qr_code = await self._qr_code_repository.get_qr_code(organization_id, qr_type)
        if not qr_code:
            raise ValueError(f"No QR code found for organization {organization_id} and type {qr_type}")
        
        qr_code.is_active = False
        return await self._qr_code_repository.update_qr_code(qr_code) 