from app.domain.repositories.worker_repository import IWorkerRepository
from app.domain.entities.worker import Worker
from app.domain.entities.worker_payment import WorkerPayment
from typing import List

class CreateWorker:
    def __init__(self, repo: IWorkerRepository):
        self.repo = repo
    async def __call__(self, worker: Worker) -> Worker:
        return await self.repo.create(worker)

class UpdateWorker:
    def __init__(self, repo: IWorkerRepository):
        self.repo = repo
    async def __call__(self, worker: Worker) -> Worker:
        return await self.repo.update(worker)

class ListWorkers:
    def __init__(self, repo: IWorkerRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Worker]:
        return await self.repo.get_all(business_id)

class RegisterPayment:
    def __init__(self, repo: IWorkerRepository):
        self.repo = repo
    async def __call__(self, payment: WorkerPayment) -> WorkerPayment:
        return await self.repo.register_payment(payment)
