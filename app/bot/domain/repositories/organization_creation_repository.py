from abc import ABC, abstractmethod
from typing import Optional
from ..models.organization_creation import OrganizationCreation

class OrganizationCreationRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[OrganizationCreation]:
        pass

    @abstractmethod
    async def save(self, organization_creation: OrganizationCreation) -> OrganizationCreation:
        pass

    @abstractmethod
    async def update(self, organization_creation: OrganizationCreation) -> OrganizationCreation:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass 