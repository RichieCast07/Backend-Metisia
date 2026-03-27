from app.domain.repositories.product_repository import IProductRepository
from app.domain.entities.product import Product
from typing import List

class CreateProduct:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
    async def __call__(self, product: Product) -> Product:
        return await self.repo.create(product)

class UpdateProduct:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
    async def __call__(self, product: Product) -> Product:
        return await self.repo.update(product)

class DeleteProduct:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
    async def __call__(self, id: str, business_id: str) -> bool:
        return await self.repo.delete(id, business_id)

class ListProducts:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
    async def __call__(self, business_id: str) -> List[Product]:
        return await self.repo.get_all(business_id)

class GetProduct:
    def __init__(self, repo: IProductRepository):
        self.repo = repo
    async def __call__(self, id: str, business_id: str) -> Product:
        return await self.repo.get_by_id(id, business_id)
