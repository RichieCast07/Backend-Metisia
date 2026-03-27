from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.domain.entities.product import Product as ProductEntity
from app.domain.repositories.product_repository import IProductRepository
from app.infrastructure.models.product import Product as ProductModel
from typing import Optional, List

class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, business_id: str) -> Optional[ProductEntity]:
        stmt = select(ProductModel).where(ProductModel.id == id, ProductModel.business_id == business_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()
        return ProductEntity(**product.__dict__) if product else None

    async def get_all(self, business_id: str) -> List[ProductEntity]:
        stmt = select(ProductModel).where(ProductModel.business_id == business_id)
        result = await self.session.execute(stmt)
        return [ProductEntity(**p.__dict__) for p in result.scalars().all()]

    async def create(self, entity: ProductEntity) -> ProductEntity:
        product = ProductModel(**entity.__dict__)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return ProductEntity(**product.__dict__)

    async def update(self, entity: ProductEntity) -> ProductEntity:
        await self.session.execute(update(ProductModel).where(ProductModel.id == entity.id).values(**entity.__dict__))
        await self.session.commit()
        return entity

    async def delete(self, id: str, business_id: str) -> bool:
        await self.session.execute(delete(ProductModel).where(ProductModel.id == id, ProductModel.business_id == business_id))
        await self.session.commit()
        return True
