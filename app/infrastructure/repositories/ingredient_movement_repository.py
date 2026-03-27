from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.ingredient_movement import IngredientMovement as IngredientMovementEntity
from app.domain.repositories.ingredient_movement_repository import IIngredientMovementRepository
from app.infrastructure.models.ingredient_movement import IngredientMovement as IngredientMovementModel
from typing import Optional, List

class IngredientMovementRepository(IIngredientMovementRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[IngredientMovementEntity]:
        stmt = select(IngredientMovementModel).where(IngredientMovementModel.id == id, IngredientMovementModel.business_id == business_id)
        result = await self.session.execute(stmt)
        im = result.scalar_one_or_none()
        return IngredientMovementEntity(**im.__dict__) if im else None

    async def get_all(self, business_id: str) -> List[IngredientMovementEntity]:
        stmt = select(IngredientMovementModel).where(IngredientMovementModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [IngredientMovementEntity(**im.__dict__) for im in result.scalars().all()]

    async def create(self, entity: IngredientMovementEntity) -> IngredientMovementEntity:
        im = IngredientMovementModel(**entity.__dict__)
        self.session.add(im)
        await self.session.commit()
        await self.session.refresh(im)
        return IngredientMovementEntity(**im.__dict__)

    async def update(self, entity: IngredientMovementEntity) -> IngredientMovementEntity:
        await self.session.execute(update(IngredientMovementModel).where(IngredientMovementModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(IngredientMovementModel).where(IngredientMovementModel.id == id, IngredientMovementModel.business_id == business_id))
        await self.session.commit()
        return True
