from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.worker import Worker as WorkerEntity
from app.domain.entities.worker_payment import WorkerPayment as WorkerPaymentEntity
from app.domain.repositories.worker_repository import IWorkerRepository
from app.infrastructure.models.worker import Worker as WorkerModel
from app.infrastructure.models.worker_payment import WorkerPayment as WorkerPaymentModel
from typing import Optional, List

class WorkerRepository(IWorkerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[WorkerEntity]:
        stmt = select(WorkerModel).where(WorkerModel.id == id, WorkerModel.business_id == business_id)
        result = await self.session.execute(stmt)
        worker = result.scalar_one_or_none()
        return WorkerEntity(**worker.__dict__) if worker else None

    async def get_all(self, business_id: str) -> List[WorkerEntity]:
        stmt = select(WorkerModel).where(WorkerModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [WorkerEntity(**w.__dict__) for w in result.scalars().all()]

    async def create(self, entity: WorkerEntity) -> WorkerEntity:
        worker = WorkerModel(**entity.__dict__)
        self.session.add(worker)
        await self.session.commit()
        await self.session.refresh(worker)
        return WorkerEntity(**worker.__dict__)

    async def update(self, entity: WorkerEntity) -> WorkerEntity:
        await self.session.execute(update(WorkerModel).where(WorkerModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(WorkerModel).where(WorkerModel.id == id, WorkerModel.business_id == business_id))
        await self.session.commit()
        return True

    async def register_payment(self, payment: WorkerPaymentEntity) -> WorkerPaymentEntity:
        wp = WorkerPaymentModel(**payment.__dict__)
        self.session.add(wp)
        await self.session.commit()
        await self.session.refresh(wp)
        return WorkerPaymentEntity(**wp.__dict__)
