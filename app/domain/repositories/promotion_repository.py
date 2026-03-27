from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.promotion import Promotion

class IPromotionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Promotion]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Promotion]: ...

    @abstractmethod
    async def create(self, entity: Promotion) -> Promotion: ...

    @abstractmethod
    async def update(self, entity: Promotion) -> Promotion: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
