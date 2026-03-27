from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.product import Product

class IProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Product]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Product]: ...

    @abstractmethod
    async def create(self, entity: Product) -> Product: ...

    @abstractmethod
    async def update(self, entity: Product) -> Product: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
