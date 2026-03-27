from app.domain.repositories.sale_repository import ISaleRepository
from app.domain.entities.sale import Sale
from app.domain.entities.sale_item import SaleItem
from app.domain.entities.worker_participation import WorkerParticipation
from typing import List

class CreateSale:
    def __init__(self, repo: ISaleRepository):
        self.repo = repo
    async def __call__(self, sale: Sale, items: List[SaleItem], participations: List[WorkerParticipation]) -> Sale:
        return await self.repo.create_with_items(sale, items, participations)

class ListSales:
    def __init__(self, repo: ISaleRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Sale]:
        return await self.repo.get_all(business_id)

class GetSale:
    def __init__(self, repo: ISaleRepository):
        self.repo = repo
    async def __call__(self, id: str, business_id: str) -> Sale:
        return await self.repo.get_by_id(id, business_id)
