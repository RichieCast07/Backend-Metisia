from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.cash_register import CashRegister

class ICashRegisterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[CashRegister]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[CashRegister]: ...

    @abstractmethod
    async def create(self, entity: CashRegister) -> CashRegister: ...

    @abstractmethod
    async def update(self, entity: CashRegister) -> CashRegister: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
