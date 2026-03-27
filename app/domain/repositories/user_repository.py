from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[User]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[User]: ...

    @abstractmethod
    async def create(self, entity: User) -> User: ...

    @abstractmethod
    async def update(self, entity: User) -> User: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...
