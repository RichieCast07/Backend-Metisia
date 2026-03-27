from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.promotion import Promotion as PromotionEntity
from app.domain.repositories.promotion_repository import IPromotionRepository
from app.infrastructure.models.promotion import Promotion as PromotionModel
from typing import Optional, List

class PromotionRepository(IPromotionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[PromotionEntity]:
        stmt = select(PromotionModel).where(PromotionModel.id == id, PromotionModel.business_id == business_id)
        result = await self.session.execute(stmt)
        promo = result.scalar_one_or_none()
        return PromotionEntity(**promo.__dict__) if promo else None

    async def get_all(self, business_id: str) -> List[PromotionEntity]:
        stmt = select(PromotionModel).where(PromotionModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [PromotionEntity(**p.__dict__) for p in result.scalars().all()]

    async def create(self, entity: PromotionEntity) -> PromotionEntity:
        promo = PromotionModel(**entity.__dict__)
        self.session.add(promo)
        await self.session.commit()
        await self.session.refresh(promo)
        return PromotionEntity(**promo.__dict__)

    async def update(self, entity: PromotionEntity) -> PromotionEntity:
        await self.session.execute(update(PromotionModel).where(PromotionModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(PromotionModel).where(PromotionModel.id == id, PromotionModel.business_id == business_id))
        await self.session.commit()
        return True
