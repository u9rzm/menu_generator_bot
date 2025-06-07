from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class Repository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: int, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass 