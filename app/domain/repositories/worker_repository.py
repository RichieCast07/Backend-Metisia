from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.worker import Worker
from app.domain.entities.worker_payment import WorkerPayment

class IWorkerRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str, business_id: str) -> Optional[Worker]: ...

    @abstractmethod
    async def get_all(self, business_id: str) -> List[Worker]: ...

    @abstractmethod
    async def create(self, entity: Worker) -> Worker: ...

    @abstractmethod
    async def update(self, entity: Worker) -> Worker: ...

    @abstractmethod
    async def delete(self, id: str, business_id: str) -> bool: ...

    @abstractmethod
    async def register_payment(self, payment: WorkerPayment) -> WorkerPayment: ...
