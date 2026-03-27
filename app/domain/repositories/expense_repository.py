from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.expense import Expense

class IExpenseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Expense]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Expense]: ...

    @abstractmethod
    async def create(self, entity: Expense) -> Expense: ...

    @abstractmethod
    async def update(self, entity: Expense) -> Expense: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
