from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.cash_register import CashRegister as CashRegisterEntity
from app.domain.repositories.cash_register_repository import ICashRegisterRepository
from app.infrastructure.models.cash_register import CashRegister as CashRegisterModel
from typing import Optional, List

class CashRegisterRepository(ICashRegisterRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[CashRegisterEntity]:
        stmt = select(CashRegisterModel).where(CashRegisterModel.id == id, CashRegisterModel.business_id == business_id)
        result = await self.session.execute(stmt)
        cr = result.scalar_one_or_none()
        return CashRegisterEntity(**cr.__dict__) if cr else None

    async def get_all(self, business_id: str) -> List[CashRegisterEntity]:
        stmt = select(CashRegisterModel).where(CashRegisterModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [CashRegisterEntity(**cr.__dict__) for cr in result.scalars().all()]

    async def create(self, entity: CashRegisterEntity) -> CashRegisterEntity:
        cr = CashRegisterModel(**entity.__dict__)
        self.session.add(cr)
        await self.session.commit()
        await self.session.refresh(cr)
        return CashRegisterEntity(**cr.__dict__)

    async def update(self, entity: CashRegisterEntity) -> CashRegisterEntity:
        await self.session.execute(update(CashRegisterModel).where(CashRegisterModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(CashRegisterModel).where(CashRegisterModel.id == id, CashRegisterModel.business_id == business_id))
        await self.session.commit()
        return True
