from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.product_ingredient import ProductIngredient

class IProductIngredientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[ProductIngredient]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[ProductIngredient]: ...

    @abstractmethod
    async def create(self, entity: ProductIngredient) -> ProductIngredient: ...

    @abstractmethod
    async def update(self, entity: ProductIngredient) -> ProductIngredient: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
