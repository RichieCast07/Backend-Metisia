from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.ingredient import Ingredient

class IIngredientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Ingredient]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Ingredient]: ...

    @abstractmethod
    async def create(self, entity: Ingredient) -> Ingredient: ...

    @abstractmethod
    async def update(self, entity: Ingredient) -> Ingredient: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
