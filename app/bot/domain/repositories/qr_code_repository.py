from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.qr_code import QRCode, QRCodeType

class QRCodeRepository(ABC):
    @abstractmethod
    async def save_qr_code(self, qr_code: QRCode) -> QRCode:
        pass

    @abstractmethod
    async def get_qr_code(self, organization_id: int, qr_type: QRCodeType) -> Optional[QRCode]:
        pass

    @abstractmethod
    async def get_all_qr_codes(self, organization_id: int) -> List[QRCode]:
        pass

    @abstractmethod
    async def update_qr_code(self, qr_code: QRCode) -> QRCode:
        pass

    @abstractmethod
    async def delete_qr_code(self, organization_id: int, qr_type: QRCodeType) -> bool:
        pass

    @abstractmethod
    async def get_active_qr_codes(self, organization_id: int) -> List[QRCode]:
        pass 