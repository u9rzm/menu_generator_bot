from typing import Optional, List, Dict
from ...domain.models.qr_code import QRCode, QRCodeType
from ...domain.services.qr_code_service import QRCodeService

class ManageQRCodeUseCase:
    def __init__(self, qr_code_service: QRCodeService):
        self._qr_code_service = qr_code_service

    async def generate_qr_code(self, organization_id: int, qr_type: QRCodeType, 
                             content: str, expires_in_days: Optional[int] = None,
                             metadata: Optional[Dict] = None) -> QRCode:
        """Generate a new QR code for an organization"""
        return await self._qr_code_service.generate_qr_code(
            organization_id=organization_id,
            qr_type=qr_type,
            content=content,
            expires_in_days=expires_in_days,
            metadata=metadata
        )

    async def get_qr_code(self, organization_id: int, qr_type: QRCodeType) -> Optional[QRCode]:
        """Get a QR code for an organization"""
        return await self._qr_code_service.get_qr_code(organization_id, qr_type)

    async def get_all_qr_codes(self, organization_id: int) -> List[QRCode]:
        """Get all QR codes for an organization"""
        return await self._qr_code_service.get_all_qr_codes(organization_id)

    async def get_active_qr_codes(self, organization_id: int) -> List[QRCode]:
        """Get all active QR codes for an organization"""
        return await self._qr_code_service.get_active_qr_codes(organization_id)

    async def update_qr_code(self, qr_code: QRCode) -> QRCode:
        """Update an existing QR code"""
        return await self._qr_code_service.update_qr_code(qr_code)

    async def delete_qr_code(self, organization_id: int, qr_type: QRCodeType) -> bool:
        """Delete a QR code"""
        return await self._qr_code_service.delete_qr_code(organization_id, qr_type)

    async def deactivate_qr_code(self, organization_id: int, qr_type: QRCodeType) -> QRCode:
        """Deactivate a QR code"""
        return await self._qr_code_service.deactivate_qr_code(organization_id, qr_type) 