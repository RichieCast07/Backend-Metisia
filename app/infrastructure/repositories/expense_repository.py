from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.expense import Expense as ExpenseEntity
from app.domain.repositories.expense_repository import IExpenseRepository
from app.infrastructure.models.expense import Expense as ExpenseModel
from typing import Optional, List

class ExpenseRepository(IExpenseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[ExpenseEntity]:
        stmt = select(ExpenseModel).where(ExpenseModel.id == id, ExpenseModel.business_id == business_id)
        result = await self.session.execute(stmt)
        expense = result.scalar_one_or_none()
        return ExpenseEntity(**expense.__dict__) if expense else None

    async def get_all(self, business_id: str) -> List[ExpenseEntity]:
        stmt = select(ExpenseModel).where(ExpenseModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [ExpenseEntity(**e.__dict__) for e in result.scalars().all()]

    async def create(self, entity: ExpenseEntity) -> ExpenseEntity:
        expense = ExpenseModel(**entity.__dict__)
        self.session.add(expense)
        await self.session.commit()
        await self.session.refresh(expense)
        return ExpenseEntity(**expense.__dict__)

    async def update(self, entity: ExpenseEntity) -> ExpenseEntity:
        await self.session.execute(update(ExpenseModel).where(ExpenseModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(ExpenseModel).where(ExpenseModel.id == id, ExpenseModel.business_id == business_id))
        await self.session.commit()
        return True
