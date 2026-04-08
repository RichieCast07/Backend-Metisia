from app.domain.repositories.promotion_repository import IPromotionRepository
from app.domain.entities.promotion import Promotion
from typing import List


class CreatePromotion:
    def __init__(self, repo: IPromotionRepository):
        self.repo = repo

    async def __call__(self, promotion: Promotion) -> Promotion:
        return await self.repo.create(promotion)


class ListPromotions:
    def __init__(self, repo: IPromotionRepository):
        self.repo = repo

    async def __call__(self, business_id: str) -> List[Promotion]:
        return await self.repo.get_all(business_id)


class GetPromotion:
    def __init__(self, repo: IPromotionRepository):
        self.repo = repo

    async def __call__(self, id: str, business_id: str) -> Promotion:
        return await self.repo.get_by_id(id, business_id)


class TogglePromotion:
    def __init__(self, repo: IPromotionRepository):
        self.repo = repo

    async def __call__(self, id: str, business_id: str) -> Promotion:
        promotion = await self.repo.get_by_id(id, business_id)
        if promotion is None:
            return None
        promotion.is_active = not promotion.is_active
        return await self.repo.update(promotion)


class DeletePromotion:
    def __init__(self, repo: IPromotionRepository):
        self.repo = repo

    async def __call__(self, id: str, business_id: str) -> bool:
        return await self.repo.delete(id, business_id)
