from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.worker_participation import WorkerParticipation

class ISaleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Sale]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Sale]: ...

    @abstractmethod
    async def create(self, entity: Sale) -> Sale: ...

    @abstractmethod
    async def update(self, entity: Sale) -> Sale: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...

    @abstractmethod
    async def create_with_items(self, sale: Sale, items: List[SaleItem], participations: List[WorkerParticipation]) -> Sale: ...
