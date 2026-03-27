from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.ingredient import Ingredient as IngredientEntity
from app.domain.repositories.ingredient_repository import IIngredientRepository
from app.infrastructure.models.ingredient import Ingredient as IngredientModel
from typing import Optional, List

class IngredientRepository(IIngredientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[IngredientEntity]:
        stmt = select(IngredientModel).where(IngredientModel.id == id, IngredientModel.business_id == business_id)
        result = await self.session.execute(stmt)
        ingredient = result.scalar_one_or_none()
        return IngredientEntity(**ingredient.__dict__) if ingredient else None

    async def get_all(self, business_id: str) -> List[IngredientEntity]:
        stmt = select(IngredientModel).where(IngredientModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [IngredientEntity(**i.__dict__) for i in result.scalars().all()]

    async def create(self, entity: IngredientEntity) -> IngredientEntity:
        ingredient = IngredientModel(**entity.__dict__)
        self.session.add(ingredient)
        await self.session.commit()
        await self.session.refresh(ingredient)
        return IngredientEntity(**ingredient.__dict__)

    async def update(self, entity: IngredientEntity) -> IngredientEntity:
        await self.session.execute(update(IngredientModel).where(IngredientModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(IngredientModel).where(IngredientModel.id == id, IngredientModel.business_id == business_id))
        await self.session.commit()
        return True
