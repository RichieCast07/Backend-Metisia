from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.ingredient_movement import IngredientMovement

class IIngredientMovementRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[IngredientMovement]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[IngredientMovement]: ...

    @abstractmethod
    async def create(self, entity: IngredientMovement) -> IngredientMovement: ...

    @abstractmethod
    async def update(self, entity: IngredientMovement) -> IngredientMovement: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
